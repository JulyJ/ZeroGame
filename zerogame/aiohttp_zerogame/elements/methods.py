from json import dumps

from ..config import log


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


async def kick_user(session):
    if session in session.room.members:
        session.room.members.remove(session)
        log.debug('user {u} left room {r}'.format(
            u=session.id,
            r=session.room.uuid
        ))


async def add_user(room, session):
    room.members.append(session)
    log.debug('user {u} joined room {r}'.format(
        u=session.id,
        r=room.uuid
    ))


async def get_random_item(db, name):
    pipeline = [{'$sample': {'size': 1}}]
    async for doc in db[name].aggregate(pipeline):
        return doc