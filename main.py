import requests
import asyncio
from pyrogram import Client as Bot, filters
from callsmusic import run, callsmusic # callsmusic import kiya
from config import API_ID, API_HASH, BOT_TOKEN, BG_IMAGE

# --- UNIVERSAL FIX FOR 'edited' ---
if not hasattr(filters, "edited"):
    filters.edited = filters.create(lambda _, __, ___: False)

# Aapka Session String
STRING_SESSION = "BQJBLZQAOy4ydKZNdb336ahf4V0P86NODeLnIq_oeGJdrBkkyQtxJZqMs_dfL2G182Q5fdt4umF-WOCqke0HVzBIb9igvqdjhKlQci5FnpS8kPIazGOSGIVYlULAttLyvFp0_fji4Xv43fC6HiKAonspmBLGQo1wQGOxkv-K8vGsbpPyEbnGjKTIUrzVyqmR5IuDFSLULLP4d0c5wsE4xL6seY9YxLTO88cbWbRV0mDRILhdJ8m6ZXve3dgS70HwxEYe9btcbYVDYFnhU_fz7dkz4M-VPivvfxIBwQRoWVeKVZTpOz0sCK5tzA3KducVy6GU6Zt3WTaU3-cDR7VUiDGa7d6iwgAAAAH_5sbSAA"

response = requests.get(BG_IMAGE)
with open("./etc/foreground.png", "wb") as file:
    file.write(response.content)

bot = Bot(
    ":memory:",
    API_ID,
    API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="handlers"),
)

# Assistant (USER) ko manually setup kar rahe hain taaki login na maange
# callsmusic.client ko hum override kar rahe hain
from callsmusic.callsmusic import client as Assistant
Assistant.api_id = API_ID
Assistant.api_hash = API_HASH
Assistant.session_string = STRING_SESSION

print("[INFO]: CYBERMUSIC STARTED!")

async def start_services():
    await bot.start()
    # Assistant ko start kar rahe hain
    await Assistant.start()
    print("[INFO]: ASSISTANT STARTED!")
    run() # Calls start karega

if __name__ == "__main__":
    # Async loop handle karne ke liye
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_services())
