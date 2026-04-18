import asyncio
import random
import re
import logging
from telethon import TelegramClient
from telethon.errors import FloodWaitError, UserBannedInChannelError, ChatWriteForbiddenError
from telethon.tl import functions, types

# ─── Настройки ───────────────────────────────────────────────────────────────
API_ID = 30654977
API_HASH = "921be05f47930bd6e60860faa4c6b0d5"
SESSION_NAME = "sender_session"

CHATS = [
    "@forum_nft_uzbekistan",
    "@gift_kurs",
    "@prem_kere",
    "@oldgroupmarketss",
    "@oldi_sotuv",
    "@stars_chatku",
    "@nodir_forum",
    "@Evbo_stars_chati",
    "@forumjon",
    "@uzfor_savdo",
    "@Savdo_Forumuzb",
    "@forumu_savdo",
    "@forum_ok",
    "@playtextuzb10",
    "@kanal_grlar_savdosi",
    "@vz_reak_rek_tekin",
    "@Onlayn_savdo_p2p",
    "@oldi_sotuv",
    "@foydalichatku",
    "@faruxs",
    "@ok_savdo",
    "@rubl_savdo_uzfor",
    "@uzforum_guruh",
    "@UsaForumGarant",
    "@nft_forumi",
    "@sales_chat",
    "@garantliy",
    "@global_forums",
    "@pikrchichat",
    "@uzfor_sovdo",
    "@uzforum_garandi",
    "@nft_savdotez",
]

INTERVAL = 480
DELAY_MIN = 25
DELAY_MAX = 45

RAW_MESSAGE = """\
<emoji id=5819154994967874788>🧑‍💻</emoji> Assalomu Aleykum!

<emoji id=5235755963515959900>🔥</emoji> <b>STARS NARXLARI HAQIDA MA'LUMOT</b> <emoji id=5244628717409439861>⚡️</emoji>

<emoji id=4920593664222168414>🌟</emoji> Telegram yulduzlari narxlari

<emoji id=5276410865514471688>⭐️</emoji> 50 ta — 10,000 so'm
<emoji id=5276410865514471688>⭐️</emoji> 100 ta — 20,000 so'm
<emoji id=5276410865514471688>⭐️</emoji> 150 ta — 30,000 so'm
<emoji id=5276410865514471688>⭐️</emoji> 200 ta — 40,000 so'm

<emoji id=5469718869536940860>👆</emoji> Eng qulay narxlar
<emoji id=5193085063998224234>🎁</emoji> Sovg'alar ham bor

➡️ @starpayuz_bot
"""

# ─── Логирование ─────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("sender.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger(__name__)


# ─── Парсер эмодзи ───────────────────────────────────────────────────────────
def parse_message(raw: str):
    entities = []
    text = ""

    token_re = re.compile(r'<emoji id=(\d+)>(.*?)</emoji>|<b>(.*?)</b>', re.DOTALL)
    last = 0

    for m in token_re.finditer(raw):
        text += raw[last:m.start()]

        if m.group(1):
            emoji_id = int(m.group(1))
            inner = m.group(2)

            offset = len(text.encode("utf-16-le")) // 2
            length = len(inner.encode("utf-16-le")) // 2

            entities.append(
                types.MessageEntityCustomEmoji(
                    offset=offset,
                    length=length,
                    document_id=emoji_id,
                )
            )
            text += inner

        elif m.group(3):
            inner = m.group(3)

            offset = len(text.encode("utf-16-le")) // 2
            length = len(inner.encode("utf-16-le")) // 2

            entities.append(types.MessageEntityBold(offset=offset, length=length))
            text += inner

        last = m.end()

    text += raw[last:]
    return text, entities


# ─── Отправка ────────────────────────────────────────────────────────────────
async def send_messages(client):
    log.info("=== Начало рассылки ===")

    text, entities = parse_message(RAW_MESSAGE)

    for chat in CHATS:
        try:
            peer = await client.get_input_entity(chat)

            await client(functions.messages.SendMessageRequest(
                peer=peer,
                message=text,
                entities=entities,
                no_webpage=True,
            ))

            log.info(f"[OK] {chat}")

        except FloodWaitError as e:
            log.warning(f"[FloodWait {e.seconds}s] {chat}")
            await asyncio.sleep(e.seconds)

        except (UserBannedInChannelError, ChatWriteForbiddenError):
            log.error(f"[NO ACCESS] {chat}")

        except Exception as e:
            log.error(f"[ERROR] {chat} — {e}")

        delay = random.randint(DELAY_MIN, DELAY_MAX)
        await asyncio.sleep(delay)

    log.info("=== Рассылка завершена ===")


# ─── MAIN ────────────────────────────────────────────────────────────────────
async def main_loop():
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

    await client.connect()

    # ❗ ВАЖНО: без этого Railway будет падать
    if not await client.is_user_authorized():
        raise Exception("❌ Сессия не найдена! Создайте её локально и загрузите.")

    log.info("✅ Клиент подключен")

    try:
        while True:
            await send_messages(client)
            log.info(f"⏳ Ждём {INTERVAL // 60} минут...")
            await asyncio.sleep(INTERVAL)

    finally:
        await client.disconnect()
        log.info("❌ Отключено")


# ─── START ───────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    asyncio.run(main_loop())