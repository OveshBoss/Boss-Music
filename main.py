import requests
import asyncio
from pyrogram import Client as Bot, filters, Client, idle
from callsmusic import callsmusic
from config import API_ID, API_HASH, BOT_TOKEN, BG_IMAGE

# --- UNIVERSAL FIX FOR 'edited' ---
if not hasattr(filters, "edited"):
    filters.edited = filters.create(lambda _, __, ___: False)

# Image Download
response = requests.get(BG_IMAGE)
with open("./etc/foreground.png", "wb") as file:
    file.write(response.content)

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

async def start_services():
    print("[INFO]: STARTING BOT...")
    await bot.start()

    print("[INFO]: STARTING ASSISTANT...")
    try:
        await Assistant.start()
        print("[INFO]: ASSISTANT LOGGED IN!")
    except Exception as e:
        print(f"[ERROR]: Assistant login failed: {e}")
        return

    # PyTgCalls Start karne ka sahi tarika
    try:
        await callsmusic.pytgcalls.start()
        print("[INFO]: PY-TGCALLS STARTED!")
    except Exception as e:
        print(f"[ERROR]: PyTgCalls failed: {e}")

    print("[INFO]: CYBERMUSIC IS NOW ONLINE!")
    await idle() # Yeh bot ko chalta rakhega
    
    # Stop services on exit
    await bot.stop()
    await Assistant.stop()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_services())
