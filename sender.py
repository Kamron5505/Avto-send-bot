import asyncio
import random
import re
import logging
from datetime import datetime
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
]

INTERVAL = 480        # 8 минут между рассылками (безопаснее чем 7)
DELAY_MIN = 25        # увеличены задержки между чатами
DELAY_MAX = 45

# Сообщение с Premium emoji и bold тегами
RAW_MESSAGE = """\
<emoji id=5819154994967874788>🧑‍💻</emoji> Assalomu Aleykum!

<emoji id=5235755963515959900>🔥</emoji> <b>STARS NARXLARI HAQIDA MA'LUMOT</b> <emoji id=5244628717409439861>⚡️</emoji>

<emoji id=4920593664222168414>🌟</emoji> Telegram yulduzlari narxlari <emoji id=5219774519056559758>⚡️</emoji>

<emoji id=5276410865514471688>⭐️</emoji> 50 ta yulduz — 10,000 so'm
<emoji id=5276410865514471688>⭐️</emoji> 100 ta yulduz — 20,000 so'm
<emoji id=5276410865514471688>⭐️</emoji> 150 ta yulduz — 30,000 so'm
<emoji id=5276410865514471688>⭐️</emoji> 200 ta yulduz — 40,000 so'm

<emoji id=5469718869536940860>👆</emoji> Eng qulay narxlar, 100% ishonchli <emoji id=5458883109430771204>✔️</emoji>
<emoji id=5193085063998224234>🎁</emoji> Sovg'alar bo'limida ham juda yaxshi takliflar bor

<emoji id=6269085886177087845>➡️</emoji> <b>Buyurtma berish:</b> @starpayuz_bot"""

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


def parse_message(raw: str):
    """
    Парсит теги <emoji id=...>текст</emoji> и <b>текст</b>
    Возвращает (plain_text, [entities])
    """
    entities = []
    text = ""
    # Токенизируем по тегам
    token_re = re.compile(
        r'<emoji id=(\d+)>(.*?)</emoji>|<b>(.*?)</b>',
        re.DOTALL
    )
    last = 0
    for m in token_re.finditer(raw):
        # Добавляем текст до тега
        text += raw[last:m.start()]
        if m.group(1):  # <emoji id=...>
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
        elif m.group(3) is not None:  # <b>
            inner = m.group(3)
            offset = len(text.encode("utf-16-le")) // 2
            length = len(inner.encode("utf-16-le")) // 2
            entities.append(
                types.MessageEntityBold(offset=offset, length=length)
            )
            text += inner
        last = m.end()
    text += raw[last:]
    return text, entities


# ─── Отправка сообщений ───────────────────────────────────────────────────────
async def send_messages(client: TelegramClient):
    log.info("=== Начало рассылки ===")
    plain_text, entities = parse_message(RAW_MESSAGE)
    success = 0
    failed = 0

    for chat in CHATS:
        try:
            peer = await client.get_input_entity(chat)
            await client(functions.messages.SendMessageRequest(
                peer=peer,
                message=plain_text,
                entities=entities,
                no_webpage=True,
            ))
            log.info(f"[OK] Отправлено в {chat}")
            success += 1
        except FloodWaitError as e:
            log.warning(f"[FloodWait] {chat} — ждём {e.seconds} сек.")
            await asyncio.sleep(e.seconds)
        except (UserBannedInChannelError, ChatWriteForbiddenError) as e:
            log.error(f"[Запрещено] {chat} — {e}")
            failed += 1
        except Exception as e:
            log.error(f"[Ошибка] {chat} — {e}")
            failed += 1

        if chat != CHATS[-1]:
            delay = random.randint(DELAY_MIN, DELAY_MAX)
            log.info(f"Ждём {delay} сек. перед следующим чатом...")
            await asyncio.sleep(delay)

    log.info(f"=== Рассылка завершена: {success} успешно, {failed} ошибок ===")


# ─── Основной цикл ────────────────────────────────────────────────────────────
async def main_loop():
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
    await client.start()
    log.info("Клиент запущен. Авторизация прошла успешно.")

    try:
        while True:
            await send_messages(client)
            log.info(f"Следующая рассылка через {INTERVAL // 60} мин.")
            await asyncio.sleep(INTERVAL)
    except KeyboardInterrupt:
        log.info("Остановлено пользователем.")
    finally:
        await client.disconnect()
        log.info("Клиент отключён.")


# ─── Точка входа ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    asyncio.run(main_loop())
