from telethon import TelegramClient
import asyncio
import random

# 🔑 Ваши данные
api_id = 30654977
api_hash = '921be05f47930bd6e60860faa4c6b0d5'

client = TelegramClient('session', api_id, api_hash)

# 📌 Чаты
chats = [
    '@forumu_savdo',
    '@Savdo_Forumuzb'
]

# 💎 Сообщение с эмодзи
message = """<emoji id=5819154994967874788>🧑‍💻</emoji> Assalomu Aleykum!

<emoji id=5235755963515959900>🔥</emoji> <b>STARS NARXLARI HAQIDA MA’LUMOT</b> <emoji id=5244628717409439861>⚡️</emoji>

<emoji id=4920593664222168414>🌟</emoji> Telegram yulduzlari narxlari <emoji id=5219774519056559758>⚡️</emoji>

<emoji id=5276410865514471688>⭐️</emoji> 50 ta yulduz — 12,000 so‘m  
<emoji id=5276410865514471688>⭐️</emoji> 100 ta yulduz — 24,000 so‘m  
<emoji id=5276410865514471688>⭐️</emoji> 150 ta yulduz — 36,000 so‘m  
<emoji id=5276410865514471688>⭐️</emoji> 200 ta yulduz — 48,000 so‘m  

<emoji id=5469718869536940860>👆</emoji> Eng qulay narxlar, 100% ishonchli <emoji id=5458883109430771204>✔️</emoji>  
<emoji id=5193085063998224234>🎁</emoji> Sovg‘alar bo‘limida ham juda yaxshi takliflar bor  

<emoji id=6269085886177087845>➡️</emoji> <b>Buyurtma berish:</b> @StarPayUz_bot  

━━━━━━━━━━━━━━━

<emoji id=5276130429919847610>⭐️</emoji> <b>Telegram Premium obuna</b>

<emoji id=5451985980363906293>🇺🇿</emoji> (Akkaunt orqali) <emoji id=5235826903490764103>🎁</emoji>

<emoji id=5276130429919847610>⭐️</emoji> 1 oy — 45,000 so‘m <emoji id=5276008899525243526>✔️</emoji>  
<emoji id=5276130429919847610>⭐️</emoji> 1 yil — 290,000 so‘m <emoji id=5276008899525243526>✔️</emoji>  

(Akkauntga kirmasdan) <emoji id=5427225953463972959>🎁</emoji>

<emoji id=5429263077927300012>🎁</emoji> 3 oy — 160,000 so‘m <emoji id=5208880351690112495>✅</emoji>  
<emoji id=5427315847129478207>🎁</emoji> 6 oy — 225,000 so‘m <emoji id=5208734533255445288>✅</emoji>  
<emoji id=5427315847129478207>🎁</emoji> 12 oy — 380,000 so‘m <emoji id=5208869687286316655>✅</emoji>  

━━━━━━━━━━━━━━━

<emoji id=5372981976804366741>🤖</emoji> Bot: @StarPayUz_bot
"""

# 🚀 Отправка
async def send_messages():
    for chat in chats:
        try:
            await client.send_message(chat, message, parse_mode='html')
            print(f"✅ Отправлено в {chat}")
            await asyncio.sleep(random.randint(15, 25))  # анти-бан
        except Exception as e:
            print(f"❌ Ошибка: {e}")

# 🔁 Цикл каждые 7 минут
async def main_loop():
    await client.start()
    while True:
        print("🚀 Начинаю рассылку...")
        await send_messages()
        print("⏳ Жду 7 минут...\n")
        await asyncio.sleep(420)

# ⚡ FIX для Windows
if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main_loop())