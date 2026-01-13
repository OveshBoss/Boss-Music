# Don't Remove Credit @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot @Tech_VJ

import requests
import asyncio
import os
import re
from pyrogram import Client as Bot, filters, Client, idle
from pyrogram.errors import FloodWait
from callsmusic import callsmusic
from config import API_ID, API_HASH, BOT_TOKEN, BG_IMAGE
from flask import Flask
from threading import Thread

# --- WEB SERVER FOR RENDER (Port Error Fix) ---
app = Flask('')
@app.route('/')
def home(): return "Bot is Alive!"
def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
def keep_alive():
    Thread(target=run).start()

# --- CONFIGURATION ---
# Welcome Image Jo Aapne Di Thi
START_PIC = "https://graph.org/file/05ab71be0729b63e0e64e-39a439939619be48cc.jpg"
DB_CAPTION = {}

# --- UNIVERSAL FIX FOR 'edited' ---
if not hasattr(filters, "edited"):
    filters.edited = filters.create(lambda _, __, ___: False)

# Image Download for Music
try:
    response = requests.get(BG_IMAGE)
    with open("./etc/foreground.png", "wb") as file:
        file.write(response.content)
except Exception as e:
    print(f"Background image download failed: {e}")

# Main Bot Client
bot = Bot(
    name="OveshBossBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="handlers"),
)

# Assistant Client
STRING_SESSION = "BQJBLZQAOy4ydKZNdb336ahf4V0P86NODeLnIq_oeGJdrBkkyQtxJZqMs_dfL2G182Q5fdt4umF-WOCqke0HVzBIb9igvqdjhKlQci5FnpS8kPIazGOSGIVYlULAttLyvFp0_fji4Xv43fC6HiKAonspmBLGQo1wQGOxkv-K8vGsbpPyEbnGjKTIUrzVyqmR5IuDFSLULLP4d0c5wsE4xL6seY9YxLTO88cbWbRV0mDRILhdJ8m6ZXve3dgS70HwxEYe9btcbYVDYFnhU_fz7dkz4M-VPivvfxIBwQRoWVeKVZTpOz0sCK5tzA3KducVy6GU6Zt3WTaU3-cDR7VUiDGa7d6iwgAAAAH_5sbSAA"

Assistant = Client(
    name="Assistant",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=STRING_SESSION
)

callsmusic.client = Assistant

# --- AI AUTOCAPTION LOGIC ---
def ai_parser(file_name):
    data = {"quality": "Unknown", "language": "N/A", "year": "N/A", "season": "01", "episode": "01", "format": "N/A"}
    q = re.search(r'480p|720p|1080p|2160p|4k', file_name, re.I)
    if q: data["quality"] = q.group()
    y = re.search(r'(19|20)\d{2}', file_name)
    if y: data["year"] = y.group()
    if re.search(r'hindi|hin', file_name, re.I): data["language"] = "Hindi"
    elif re.search(r'english|eng|en', file_name, re.I): data["language"] = "English"
    se = re.search(r'S(\d+).?E(\d+)', file_name, re.I)
    if se: data["season"], data["episode"] = se.group(1), se.group(2)
    if "." in file_name: data["format"] = file_name.split(".")[-1].upper()
    return data

def get_size(size):
    if not size: return "0 B"
    for unit in ['B','KB','MB','GB','TB']:
        if size < 1024: return f"{size:.2f} {unit}"
        size /= 1024

# --- HANDLERS ---

@bot.on_message(filters.command("start") & filters.private)
async def start_cmd(client, message):
    me = await client.get_me()
    buttons = [
        [pyrogram.types.InlineKeyboardButton("📥 ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ᴄʜᴀɴɴᴇʟ 📥", url=f"http://t.me/{me.username}?startchannel=true")],
        [
            pyrogram.types.InlineKeyboardButton("🌤 ᴜᴘᴅᴀᴛᴇ 🌤", url="https://t.me/VJ_Botz"),
            pyrogram.types.InlineKeyboardButton("🍁 sᴜᴘᴘᴏʀᴛ 🍁", url="https://t.me/KingVJ01")
        ],
        [
            pyrogram.types.InlineKeyboardButton("ʜᴇʟᴘ ⚙️", callback_data="help_data"),
            pyrogram.types.InlineKeyboardButton("ᴀʙᴏᴜᴛ 💌", callback_data="about_data")
        ]
    ]
    await message.reply_photo(
        photo=START_PIC,
        caption=f"<b>ʜᴇʏ {message.from_user.mention} 👋 ʜᴏᴡ ᴀʀᴇ ʏᴏᴜ</b>\n\n"
                f"🔘 ɪ ᴀᴍ ᴜʟᴛʀᴀ ᴘᴏᴡᴇʀғᴜʟ ᴀᴜᴛᴏ ᴄᴀᴘᴛɪᴏɴ + ᴍᴜsɪᴄ ʙᴏᴛ\n"
                f"🔘 ɪ ᴄᴀɴ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ᴇᴅɪᴛ ғɪʟᴇ ᴄᴀᴘᴛɪᴏɴs ᴀɴᴅ ᴘʟᴀʏ ᴍᴜsɪᴄ!",
        reply_markup=pyrogram.types.InlineKeyboardMarkup(buttons)
    )

@bot.on_message(filters.channel & filters.media)
async def auto_caption_logic(client, update):
    chat_id = update.chat.id
    template = DB_CAPTION.get(chat_id, "**{file_name}**\n\n⚙️ Sɪᴢᴇ: {file_size}")
    
    file_obj = getattr(update, update.media.value)
    f_name = getattr(file_obj, 'file_name', 'File')
    f_size = get_size(getattr(file_obj, 'file_size', 0))
    ai = ai_parser(f_name)
    
    final_caption = template.format(
        file_name=f_name, file_size=f_size, quality=ai["quality"],
        language=ai["language"], year=ai["year"], season=ai["season"],
        episode=ai["episode"], format=ai["format"]
    )

    try:
        await update.edit_caption(caption=final_caption)
    except FloodWait as e:
        await asyncio.sleep(e.value)
        await update.edit_caption(caption=final_caption)
    except Exception: pass

# --- STARTUP SERVICES ---

async def start_services():
    keep_alive() # Render Port Fix
    print("[INFO]: STARTING BOT...")
    await bot.start()

    print("[INFO]: STARTING ASSISTANT...")
    try:
        await Assistant.start()
    except Exception as e:
        print(f"[ERROR]: Assistant login failed: {e}")
        return

    try:
        await callsmusic.pytgcalls.start()
        print("[INFO]: PY-TGCALLS STARTED!")
    except Exception as e:
        print(f"[ERROR]: PyTgCalls failed: {e}")

    print("[INFO]: CYBERMUSIC & AUTOCAPTION ONLINE!")
    await idle()
    await bot.stop()
    await Assistant.stop()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_services())
