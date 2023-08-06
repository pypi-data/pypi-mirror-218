#!/usr/bin/env python
"""
Example of a bot implementation.

This bot does multiple things:
- Authenticates either as guest of with (ethereum) account private key.
- Updates name an image of the account if not already set.
- Greets users entering the world, by flying towards them and sending a high-five.
- Spawns a object (cube), when receiving a high-five, changes to objects color.
- Spawns another object, with uploaded GLB model, that continuously moves around along a circular path.

"""
import contextlib
import itertools
import logging
import math
import os
import pathlib
import platform
import random
import signal
import uuid

import anyio
import asyncclick as click

from odyssey_momentum import api
from odyssey_momentum.bot import Bot, Position, World, assets

# World uses right-handed coordinates system. Y-axis is up.
# X is left, Z is forwards.
# Users enter the world at:
WORLD_SPAWN_POINT = (50, 50, 150)  # legacy coords, will become customizable...


@click.command()
@click.option("-u", "--url", "url", default="http://localhost:8080")
@click.option("-g", "--guest", "guest", default=False, is_flag=True)
@click.option("-w", "--world", "world_id", default="00000000-0000-8000-8000-000000000002")
@click.option("-v", "--verbose", "verbose", count=True)
@click.option("-b", "--beebug", "bb", default=False, is_flag=True)
async def main(url, guest, world_id, verbose, bb):
    _configure_logging(verbose)
    async with Bot(url) as bot, anyio.create_task_group() as tg, contextlib.AsyncExitStack() as exit_stack:
        tg.start_soon(signal_handler, tg.cancel_scope, name="Signal handler")
        bb and _bb()
        if guest:
            await bot.authenticate_guest()
            click.echo(f"🔒Authenticated as guest {bot.uid}.")
        else:
            account_key = os.environ["ODYSSEY_ACCOUNT_KEY"]
            await bot.authenticate(account_key)
            click.echo(f"🔒Authenticated with private key as {bot.uid}.", nl=False)

        await update_profile(bot)

        world = await bot.teleport(world_id)  # TODO: should we make this an async context? to cleanly leave a world?
        click.secho(f"Entered world {world.name}")

        # TODO: move these into the world (and make it track its own tasks
        tg.start_soon(world.track_objects, name="Track objects in world")
        tg.start_soon(world.track_users, name="Track users in world")

        click.secho("Moving to hunting perch...")  # ;p
        await world.move_bot(Position(42, 42, 192))
        click.secho("Reached location.")
        # TODO: how do we know if we have 'write' perms on the world? :/
        oid = None
        dragon_oid = None
        try:
            oid = await spawn_object_companion(world, (42, 42, 192))

            async def cleanup():
                with anyio.CancelScope(shield=True):
                    click.secho(f"cleaning up {oid} after myself...")
                    await world.remove_object(oid)

            exit_stack.push_async_callback(cleanup)

            dragon_oid = await spawn_dragon(world)

            async def cleanup_dragon():
                with anyio.CancelScope(shield=True):
                    click.secho(f"cleaning up {dragon_oid} after myself...")
                    await world.remove_object(dragon_oid)

            exit_stack.push_async_callback(cleanup_dragon)
        except api.APIPermissionDenied:
            click.secho("No permission to edit world.", fg="red")
        tg.start_soon(respond_to_h5s, world, oid, name="Respond to h5s")

        tg.start_soon(greet_users, world, name="Greet new users")

        if dragon_oid:
            tg.start_soon(dragon_patrol, world, dragon_oid, name="Dragon")

        await idler(world)

    click.secho("Stopped", fg="red", bold=True)


def _configure_logging(verbose):
    match verbose:
        case 0:
            log_level = logging.ERROR
        case 1:
            log_level = logging.INFO
        case 2:
            log_level = logging.DEBUG
            logging.getLogger("httpcore").setLevel(logging.INFO)
            logging.getLogger("httpx").setLevel(logging.INFO)
            logging.getLogger("hpack").setLevel(logging.INFO)
        case _:
            log_level = logging.DEBUG

    logging.basicConfig(level=log_level)
    logging.captureWarnings(True)


async def signal_handler(scope: anyio.CancelScope):
    with anyio.open_signal_receiver(signal.SIGINT, signal.SIGTERM) as signals:
        async for signum in signals:
            click.secho(f"Signal {signum} received, please wait while I clean up...")
            scope.cancel()


async def update_profile(bot: Bot):
    """Update the bot's account profile if its empty."""
    me = await bot.profile()
    if not me.name or not (me.profile and me.profile.avatar_hash):
        mod_path = pathlib.Path(__file__).parent
        with open(mod_path / "bot_avatar.png", mode="rb") as f:
            await bot.update_profile("Botty McBotface", f)


async def spawn_object_companion(world: World, position: tuple[float, float, float]) -> uuid.UUID:
    """Spawn a special object when this bot enters a world."""
    name = "Bot companion object"  # TODO: plugin attr to track this, instead of relying on unique name
    # TODO: racy, not async. Don't know for sure if we have all objects here yet...
    found = [o for o in world.object_list() if o.name == name]
    if len(found) > 0:
        existing = found.pop()
        if found:
            for duplicate in found:
                click.secho(f"Removing old trash {duplicate.oid} from the world.")
                await world.remove_object(duplicate.oid)
        return existing.oid
    oid = await world.spawn_object(name, assets.cube(), position=position)
    return oid


async def greet_users(world: World):
    """
    Greet users when they enter the world.

    Greeting is done by flying towards them end sending an High-five.
    """
    click.secho("Greeting user task...")
    async with world.user_stream() as users:
        async for user in users:
            click.secho(f"Going to greet user {user.uid}")
            await world.move_bot_to_user(user)
            click.secho(f"Reached user {user.uid}... h5'ing")
            await world.high_five(user)


async def respond_to_h5s(world: World, companion_obj_oid: uuid.UUID | None):
    click.secho("High-five responder task...")
    async with world.high_five_stream() as h5s:
        async for h5 in h5s:
            click.secho(f"h5 received: {h5}")
            if h5.receiver == world.bot.uid:
                if companion_obj_oid:
                    obj = await world.get_object(companion_obj_oid)
                    await obj.change_color(f"#{random.randint(0, 0xFFFFFF):06x}")


async def spawn_dragon(world: World):
    await world.bot.asset_list()
    existing_aids = [a.id for a in await world.bot.asset_list()]
    our_id = "18e266d6-d8be-89b6-547e-1aa859c4c97b"
    name = "Drago McDragonFace"
    if our_id not in existing_aids:
        mod_path = pathlib.Path(__file__).parent
        with open(mod_path / "ducky.glb", "rb") as f:
            asset = await world.bot.asset_upload(name, f)
            aid = asset["id"]
            if aid != our_id:
                click.secho(
                    f"GLB file changed! Update the expected ID to {aid}!",
                    fg="red",
                    bold=True,
                )
                our_id = aid
    found = [o for o in world.object_list() if o.name == name]
    if len(found) > 0:
        existing = found.pop()
        if found:
            for duplicate in found:
                click.secho(f"Removing old trash {duplicate.oid} from the world.")
                await world.remove_object(duplicate.oid)
        return existing.oid
    oid = await world.spawn_object(name, asset_id=our_id, position=(100, 100, 100), scale=(8, 8, 8))
    return oid


async def dragon_patrol(world: World, oid: uuid.UUID):
    """Async task that move the object around"""
    click.secho("Dragon patrol task...")
    obj = None
    while obj is None:
        await anyio.sleep(1)
        obj = await world.get_object(oid)  # TODO: make it await new obj
    elevation = WORLD_SPAWN_POINT[1] + 42
    radius = 42 * 2
    (WORLD_SPAWN_POINT[0], WORLD_SPAWN_POINT[2])
    points = itertools.cycle(_points_on_circle(radius))
    for x, z in points:
        await anyio.sleep(0.5)
        await obj.move_to((x, elevation, z))


def _points_on_circle(r, center=(0, 0), n=10):
    # ah... really need to pick a vector/matrix library to do this for you :)
    yield from (
        (
            center[0] + (math.cos(2 * math.pi / n * x) * r),
            center[1] + (math.sin(2 * math.pi / n * x) * r),
        )
        for x in range(0, n + 1)
    )


async def idler(world: World):
    """Do something when the bot is idle for a while"""
    # TODO
    click.secho("Idling task...")
    await anyio.sleep(42)
    click.secho("Idling: I'm bored... let me describe the world:")
    for _oid, o in world._objects.items():
        click.secho(f"{o.oid} {o.asset_format} {o.asset_type} {o.name}")
    for _uid, u in world._users.items():
        click.secho(f"{u.uid} {u.is_guest} {u.name}")

    await anyio.sleep_forever()


def _bb():
    # egg
    os.system("color A0") if platform.system() == "Windows" else os.system( # noqa
        "setterm -background green -foreground black -store"  # noqa
    )


if __name__ == "__main__":
    main(_anyio_backend="asyncio")
