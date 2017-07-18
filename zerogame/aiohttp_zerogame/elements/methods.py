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


async def kick_user(app, session):
    for room in app.rooms:
        if session in room.members:
            room.members.remove(session)


async def add_user(room, session):
    room.members.append(session)
