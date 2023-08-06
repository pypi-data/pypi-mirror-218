import asyncio
import contextlib
import logging
import queue
from collections.abc import AsyncGenerator, AsyncIterator, Awaitable, Callable
from typing import TypeAlias

import wsproto
from httpx_ws import AsyncWebSocketSession, WebSocketDisconnect, aconnect_ws

from . import auth, protocol, urls


class ConnectedError(Exception):
    pass


logger = logging.getLogger(__name__)

SendFunc: TypeAlias = Callable[[protocol.OutMessage], Awaitable[None]]
# TypeAlias for the incoming message generator
InGenerator: TypeAlias = AsyncGenerator[tuple[protocol.MsgType, protocol.InMessage], None]


@contextlib.asynccontextmanager
async def connect(base_url: str, auth: auth.Auth) -> AsyncIterator[tuple[SendFunc, InGenerator]]:
    """
    Connect to remote server.

    This async context manager connects to the remote (websocket)
    and yields a send function and an async generator.

    The send function can be used to send protocol messages back to the server.
    The async generator can be iterated over to receive messages.
    """
    ws_url = urls.posbus_websocket_url(base_url)
    logger.debug("Connecting to %s", ws_url)
    async with aconnect_ws(ws_url) as ws:

        async def send(msg: protocol.OutMessage):
            # print(f"Send %s", msg)
            await ws.send_bytes(protocol.encode(msg))

        hs_msg = protocol.handshake(auth)
        logger.debug("Sending handshake")
        await send(hs_msg)

        yield send, _ws_msg_generator(ws)
    logger.debug("Closed")


async def _ws_msg_generator(
    ws: AsyncWebSocketSession,
) -> InGenerator:
    # receive is uninteruptable, so workaround with timeout
    timeout = 7  # completely arbitrary
    while True:
        try:
            bs = await ws.receive_bytes(timeout=timeout)
            msg = protocol.decode(bs)
            logger.debug("Receved %s", msg)
            yield msg
        except queue.Empty:
            pass
        except asyncio.TimeoutError:
            # workaround, closing connection not detected...
            if ws.connection.state in {
                wsproto.connection.ConnectionState.LOCAL_CLOSING,
                wsproto.connection.ConnectionState.CLOSED,
            }:
                logger.debug("connection close(ing)")
                return
        except WebSocketDisconnect as e:
            logger.debug("disconnect %s", e)
            return


''' gopy client version:
@contextlib.asynccontextmanager
async def _client(base_url: str, auth: Auth):
    url = posbus_websocket_url(base_url)
    try:
        client = pbc.new_client()
        yield client
    finally:
        print("client finally")
        client.close()



@contextlib.asynccontextmanager
async def connect_pbc_client(base_url: str, auth: Auth) -> AsyncGenerator:
    async with _client(
        base_url, auth
    ) as client, anyio.create_task_group() as tg, contextlib.AsyncExitStack() as stack:
        try:
            ctx = context.background()
            user_id = umid.parse(auth["id"])

            # Handle incoming message from the cgo lib:
            cb_send_stream, cb_recv_stream = anyio.create_memory_object_stream(
                1024, posbus.Message
            )
            await stack.enter_async_context(cb_send_stream)
            await stack.enter_async_context(cb_recv_stream)

            def cb(handle):
                # tg.start_soon(cb_send_stream.send, _process_msg(handle))
                # called from c binding... not event loop(?)
                try:
                    print("recv: %s", handle)
                    cb_send_stream.send_nowait(_process_msg(handle))
                except anyio.ClosedResourceError:
                    pass

            client.set_callback(cb, goRun=False)

            send_in_stream, send_out_stream = anyio.create_memory_object_stream(
                1, posbus.Message
            )

            async def send_listener(stream):
                with stream:
                    async for msg in stream:
                        print(f"send: {msg}")
                        client.send(_process_out_msg(msg))

            tg.start_soon(send_listener, send_out_stream)

            # an export function to use for sending messages back to the server.
            async def send_receive(msg: posbus.Message):
                await send_in_stream.send(msg)

            print("Connecting...")
            url = posbus_websocket_url(base_url)
            err = client.connect(ctx, url, auth["token"], user_id)
            if err:
                raise ConnectionError(err)
            first_msg = await cb_recv_stream.receive()
            if not isinstance(first_msg, posbus.Signal):
                raise ConnectionError(f"Unexpected first message {first_msg}")
            elif not first_msg.value == posbus.SignalConnected:
                signal_type = posbus.SignalType(first_msg.value)
                raise ConnectionError(f"Connection error {signal_type}")
            print("connected.")
            yield send_receive, cb_recv_stream
        except Exception as e:
            print(f"err: {e}")
            raise e
        finally:
            print("connect finally")
            # client.close()


def _handle_incoming(client):
    """Handle incoming messages from the cgo lib."""
    # cgo lib has a callback mechanism, so we need to 'pave over' that there.
    # TODO: 'fix' the lib and give us a more flexible API :)
    cb_send_stream, cb_recv_stream = anyio.create_memory_object_stream(
        1, posbus.Message
    )

    def cb(handle):
        tg.start_soon(cb_send_stream.send, _process_msg(handle))

    client.set_callback(cb, goRun=False)
    return cb_recv_stream


def _process_msg(handle):
    msg = posbus.Message(handle=handle)
    return protocol.process_msg(msg)


def _process_out_msg(msg: protocol.Message):
    return posbus.bin_message(msg)


async def process_items(client, receive_stream):
    print("Start send io")
    async with receive_stream:
        async for item in receive_stream:
            print("send: %s" % item)
            client.send(item)
'''
