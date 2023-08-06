#!/usr/bin/env python
"""
Example of using the api and posbus modules.

Basic example, authenticates, connect and then just dumps incoming messages.
"""
import os
import pathlib

import asyncclick as click

from odyssey_momentum import api, posbus


@click.command()
@click.option("-u", "--url", "url", default="http://localhost:8080")
@click.option("-g", "--guest", "guest", default=False, is_flag=True)
@click.option("-w", "--world", "world", default="00000000-0000-8000-8000-000000000002")
async def main(url, guest, world):
    if guest:
        auth = await posbus.authenticate_guest(url)
        print(f"As guest {auth['id']}")
    else:
        key = _account_from_env()
        if key:
            account = posbus.web3_account(key)
            auth = await posbus.authenticate_web3(url, account)
            print(f"As user {auth['id']}")
        else:
            msg = "No private key found in environment"
            raise Exception(msg)

    api_client = api.API(url, auth["token"])
    me = await api_client.current_user()
    if not me.name or not (me.profile and me.profile.avatar_hash):
        mod_path = pathlib.Path(__file__).parent
        with open(mod_path / "bot_avatar.png", mode="rb") as f:
            await api_client.update_profile("Botty McBotface", f)

    async with posbus.connect(url, auth) as (send, stream):
        await send(posbus.teleport_request(world))
        async for (msg_type, msg) in stream:
            process_item(msg_type, msg)
    print("The End")


def process_item(msg_type, msg):
    match msg_type:
        case posbus.MsgType.TypeSetWorld:
            world_id = msg["id"]
            name = msg["name"]
            print(f"In world {name} ({world_id})")
        case posbus.MsgType.TypeAddObjects:
            for obj in msg["objects"]:
                name = obj["name"]
                object_id = obj["id"]
                coords = obj["transform"]["position"]
                rot = obj["transform"]["rotation"]
                scl = obj["transform"]["scale"]
                print(f"Object {name} ({object_id}) ⊹{coords} ∡{rot} ⇲{scl}")
        case posbus.MsgType.TypeObjectData:
            object_id = msg["id"]
            entries = msg["entries"]
            print(f"Data for object {object_id} {entries}")
        case posbus.MsgType.TypeAddUsers:
            for usr in msg["users"]:
              name = usr["name"]
              user_id = usr["id"]
              print(f"User {name} ({user_id})")
        case posbus.MsgType.TypeUsersTransformList:
            for usr in msg["value"]:
                user_id = usr["id"]
                coords = usr["transform"]["position"]
                rot = usr["transform"]["rotation"]
                print(f"User ({user_id}) moving ⊹{coords} ∡{rot}")
        case _:
            print(msg_type, msg)

def _account_from_env():
    return os.environ.get("ODYSSEY_ACCOUNT_KEY", None)


if __name__ == "__main__":
    main(_anyio_backend="asyncio")
