from json import dumps


async def room_broadcast(room, event):
    for member in room.members:
        member.send(await ws_message(event))


async def ws_message(message, type='chat'):
    return dumps(
        {
            'type': type,
            'message': message
        }
    )
