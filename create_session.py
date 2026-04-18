import asyncio
from telethon import TelegramClient

API_ID = 30654977
API_HASH = "921be05f47930bd6e60860faa4c6b0d5"

async def main():
    client = TelegramClient('railway_session', API_ID, API_HASH)
    await client.start()
    print('Сессия создана: railway_session.session')
    await client.disconnect()

asyncio.run(main())
