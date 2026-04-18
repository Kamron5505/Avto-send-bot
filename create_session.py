import asyncio
from telethon import TelegramClient

api_id = 30654977
api_hash = "921be05f47930bd6e60860faa4c6b0d5"

async def main():
    client = TelegramClient("sender_session", api_id, api_hash)
    
    await client.start()  # тут попросит номер и код
    
    print("✅ Session создана!")
    await client.disconnect()

asyncio.run(main())