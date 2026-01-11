import requests
from pyrogram import Client as Bot, filters # filters yahan add kiya hai
from callsmusic import run
from config import API_ID, API_HASH, BOT_TOKEN, BG_IMAGE

# --- UNIVERSAL FIX FOR 'edited' ATTRIBUTE ERROR ---
if not hasattr(filters, "edited"):
    filters.edited = filters.create(lambda _, __, ___: False)
# --------------------------------------------------

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

print("[INFO]: CYBERMUSIC STARTED!")

bot.start()
run()
