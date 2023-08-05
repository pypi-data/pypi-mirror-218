"""Back-end using NATS."""


import logging
import math
import time
from functools import partial
from typing import (
    Any,
    AsyncGenerator,
    Awaitable,
    Callable,
    List,
    Optional,
    TypeVar,
    cast,
)

import nats

from .. import broker_client_interface, log_msgs
from ..broker_client_interface import (
    RETRY_DELAY,
    TIMEOUT_MILLIS_DEFAULT,
    TRY_ATTEMPTS,
    ClosingFailedException,
    Message,
    Pub,
    RawQueue,
    Sub,
)

LOGGER = logging.getLogger("mqclient.nats")

T = TypeVar("T")  # the callable/awaitable return type


async def _anext(gen: AsyncGenerator[Any, Any], default: Any) -> Any:
    """Provide the functionality of python 3.10's `anext()`.

    https://docs.python.org/3/library/functions.html#anext
    """
    try:
        return await gen.__anext__()
    except StopAsyncIteration:
        return default


async def try_call(self: "NATS", func: Callable[..., Awaitable[T]]) -> T:
    """Call `func` with auto-retries."""
    i = 0
    while True:
        if i > 0:
            LOGGER.debug(
                f"{log_msgs.TRYCALL_CONNECTION_ERROR_TRY_AGAIN} (attempt #{i+1})..."
            )

        try:
            return await func()
        except nats.errors.TimeoutError:
            raise
        except Exception as e:  # pylint:disable=broad-except
            LOGGER.debug(f"[try_call()] Encountered exception: '{e}'")
            if i == TRY_ATTEMPTS - 1:
                LOGGER.debug(log_msgs.TRYCALL_CONNECTION_ERROR_MAX_RETRIES)
                raise

        await self.close()
        time.sleep(RETRY_DELAY)
        await self.connect()
        i += 1


class NATS(RawQueue):
    """Base NATS wrapper, using JetStream.

    Extends:
        RawQueue
    """

    def __init__(self, endpoint: str, stream_id: str, subject: str) -> None:
        super().__init__()
        LOGGER.info(
            f"Requested MQClient for stream_id/subject '{stream_id}/{subject}' @ {endpoint}"
        )

        self.endpoint = endpoint
        self.subject = subject
        self.stream_id = stream_id

        self._nats_client: Optional[nats.aio.client.Client] = None
        self.js: Optional[nats.js.JetStreamContext] = None

        LOGGER.debug(f"Stream & Subject: {stream_id}/{self.subject}")

    async def connect(self) -> None:
        """Set up connection and channel."""
        await super().connect()
        self._nats_client = await nats.connect(self.endpoint)  # type: ignore[arg-type]
        # Create JetStream context
        self.js = self._nats_client.jetstream(timeout=TIMEOUT_MILLIS_DEFAULT // 1000)
        await self.js.add_stream(name=self.stream_id, subjects=[self.subject])

    async def close(self) -> None:
        """Close connection."""
        await super().close()
        if not self._nats_client:
            raise ClosingFailedException("No connection to close.")
        await self._nats_client.close()


class NATSPub(NATS, Pub):
    """Wrapper around PublisherClient, using JetStream.

    Extends:
        NATS
        Pub
    """

    def __init__(self, endpoint: str, stream_id: str, subject: str):
        LOGGER.debug(f"{log_msgs.INIT_PUB} ({endpoint}; {stream_id}; {subject})")
        super().__init__(endpoint, stream_id, subject)
        # NATS is pub-centric, so no extra instance needed

    async def connect(self) -> None:
        """Set up pub, then create topic and any subscriptions indicated."""
        LOGGER.debug(log_msgs.CONNECTING_PUB)
        await super().connect()
        LOGGER.debug(log_msgs.CONNECTED_PUB)

    async def close(self) -> None:
        """Close pub (no-op)."""
        LOGGER.debug(log_msgs.CLOSING_PUB)
        await super().close()
        LOGGER.debug(log_msgs.CLOSED_PUB)

    async def send_message(self, msg: bytes) -> None:
        """Send a message (publish)."""
        LOGGER.debug(log_msgs.SENDING_MESSAGE)
        if not self.js:
            raise RuntimeError("JetStream is not connected")

        ack: nats.js.api.PubAck = await try_call(
            self, partial(self.js.publish, self.subject, msg)
        )
        LOGGER.debug(f"Sent Message w/ Ack: {ack}")
        LOGGER.debug(log_msgs.SENT_MESSAGE)


class NATSSub(NATS, Sub):
    """Wrapper around queue with prefetch-queue, using JetStream.

    Extends:
        NATS
        Sub
    """

    def __init__(self, endpoint: str, stream_id: str, subject: str, prefetch: int):
        LOGGER.debug(f"{log_msgs.INIT_SUB} ({endpoint}; {stream_id}; {subject})")
        super().__init__(endpoint, stream_id, subject)
        self._subscription: Optional[nats.js.JetStreamContext.PullSubscription] = None
        self._prefetch = prefetch  # see `Sub.prefetch` property

    async def connect(self) -> None:
        """Set up sub (pull subscription)."""
        LOGGER.debug(log_msgs.CONNECTING_SUB)
        await super().connect()
        if not self.js:
            raise RuntimeError("JetStream is not connected.")

        self._subscription = await self.js.pull_subscribe(self.subject, "psub")
        LOGGER.debug(log_msgs.CONNECTED_SUB)

    async def close(self) -> None:
        """Close sub."""
        LOGGER.debug(log_msgs.CLOSING_SUB)
        if not self._subscription:
            raise ClosingFailedException("No sub to close.")
        await super().close()
        LOGGER.debug(log_msgs.CLOSED_SUB)

    @staticmethod
    def _to_message(  # type: ignore[override]  # noqa: F821 # pylint: disable=W0221
        msg: nats.aio.msg.Msg,  # pylint: disable=no-member
    ) -> Optional[Message]:
        """Transform NATS-Message to Message type."""
        return Message(msg.reply, msg.data)

    def _from_message(self, msg: Message) -> nats.aio.msg.Msg:
        """Transform Message instance to NATS-Message.

        Assumes the message came from this NATSSub instance.
        """
        if not self._nats_client:
            raise RuntimeError("Client is not connected")

        return nats.aio.msg.Msg(
            _client=self._nats_client,
            subject=self.subject,
            reply=cast(str, msg.msg_id),  # we know this is str b/c `_to_message()`
            data=msg.data,
            headers=None,  # default
        )

    async def _get_messages(
        self, timeout_millis: Optional[int], num_messages: int
    ) -> List[Message]:
        """Get n messages.

        The subscriber pulls a specific number of messages. The actual
        number of messages pulled may be smaller than `num_messages`.
        """
        if not self._subscription:
            raise RuntimeError("Subscriber is not connected")

        if not timeout_millis:
            timeout_millis = TIMEOUT_MILLIS_DEFAULT

        try:
            nats_msgs: List[nats.aio.msg.Msg] = await try_call(
                self,
                partial(
                    self._subscription.fetch,
                    num_messages,
                    int(math.ceil(timeout_millis / 1000)),
                ),
            )
        except nats.errors.TimeoutError:
            return []

        msgs = []
        for recvd in nats_msgs:
            msg = self._to_message(recvd)
            if msg:
                msgs.append(msg)
        return msgs

    async def get_message(
        self, timeout_millis: Optional[int] = TIMEOUT_MILLIS_DEFAULT
    ) -> Optional[Message]:
        """Get a message."""
        LOGGER.debug(log_msgs.GETMSG_RECEIVE_MESSAGE)
        if not self._subscription:
            raise RuntimeError("Subscriber is not connected.")

        try:
            msg = (await self._get_messages(timeout_millis, 1))[0]
            LOGGER.debug(f"{log_msgs.GETMSG_RECEIVED_MESSAGE} ({msg}).")
            return msg
        except IndexError:
            LOGGER.debug(log_msgs.GETMSG_NO_MESSAGE)
            return None

    async def _gen_messages(
        self, timeout_millis: Optional[int], num_messages: int
    ) -> AsyncGenerator[Message, None]:
        """Continuously generate messages until there are no more."""
        if not self._subscription:
            raise RuntimeError("Subscriber is not connected.")

        while True:
            msgs = await self._get_messages(timeout_millis, num_messages)
            if not msgs:
                return
            for msg in msgs:
                yield msg

    async def ack_message(self, msg: Message) -> None:
        """Ack a message from the queue."""
        LOGGER.debug(log_msgs.ACKING_MESSAGE)
        if not self._subscription:
            raise RuntimeError("subscriber is not connected")

        # Acknowledges the received messages so they will not be sent again.
        await try_call(self, partial(self._from_message(msg).ack))
        LOGGER.debug(f"{log_msgs.ACKED_MESSAGE} ({msg.msg_id!r}).")

    async def reject_message(self, msg: Message) -> None:
        """Reject (nack) a message from the queue."""
        LOGGER.debug(log_msgs.NACKING_MESSAGE)
        if not self._subscription:
            raise RuntimeError("subscriber is not connected")

        await try_call(self, partial(self._from_message(msg).nak))  # yes, it's "nak"
        LOGGER.debug(f"{log_msgs.NACKED_MESSAGE} ({msg.msg_id!r}).")

    async def message_generator(
        self, timeout: int = 60, propagate_error: bool = True
    ) -> AsyncGenerator[Optional[Message], None]:
        """Yield Messages.

        Generate messages with variable timeout.
        Yield `None` on `throw()`.

        Keyword Arguments:
            timeout {int} -- timeout in seconds for inactivity (default: {60})
            propagate_error {bool} -- should errors from downstream code kill the generator? (default: {True})
        """
        LOGGER.debug(log_msgs.MSGGEN_ENTERED)
        if not self._subscription:
            raise RuntimeError("subscriber is not connected")

        msg = None
        try:
            gen = self._gen_messages(timeout * 1000, self.prefetch)
            while True:
                # get message
                LOGGER.debug(log_msgs.MSGGEN_GET_NEW_MESSAGE)
                msg = await _anext(gen, None)
                if msg is None:
                    LOGGER.info(log_msgs.MSGGEN_NO_MESSAGE_LOOK_BACK_IN_QUEUE)
                    break

                # yield message to consumer
                try:
                    LOGGER.debug(f"{log_msgs.MSGGEN_YIELDING_MESSAGE} [{msg}]")
                    yield msg
                # consumer throws Exception...
                except Exception as e:  # pylint: disable=W0703
                    LOGGER.debug(log_msgs.MSGGEN_DOWNSTREAM_ERROR)
                    if propagate_error:
                        LOGGER.debug(log_msgs.MSGGEN_PROPAGATING_ERROR)
                        raise
                    LOGGER.warning(
                        f"{log_msgs.MSGGEN_EXCEPTED_DOWNSTREAM_ERROR} {e}.",
                        exc_info=True,
                    )
                    yield None  # hand back to consumer
                # consumer requests again, aka next()
                else:
                    pass

        # garbage collection (or explicit generator close(), or break in consumer's loop)
        except GeneratorExit:
            LOGGER.debug(log_msgs.MSGGEN_GENERATOR_EXITING)
            LOGGER.debug(log_msgs.MSGGEN_GENERATOR_EXITED)


class BrokerClient(broker_client_interface.BrokerClient):
    """NATS Pub-Sub BrokerClient Factory.

    Extends:
        BrokerClient
    """

    NAME = "nats"

    @staticmethod
    async def create_pub_queue(
        address: str,
        name: str,
        auth_token: str,
        ack_timeout: Optional[int],
    ) -> NATSPub:
        """Create a publishing queue.

        # NOTE - `auth_token` is not used currently
        """
        q = NATSPub(  # pylint: disable=invalid-name
            address,
            name + "-stream",
            name + "-subject",
        )
        await q.connect()
        return q

    @staticmethod
    async def create_sub_queue(
        address: str,
        name: str,
        prefetch: int,
        auth_token: str,
        ack_timeout: Optional[int],
    ) -> NATSSub:
        """Create a subscription queue.

        # NOTE - `auth_token` is not used currently
        """
        q = NATSSub(  # pylint: disable=invalid-name
            address,
            name + "-stream",
            name + "-subject",
            prefetch,
        )
        await q.connect()
        return q
