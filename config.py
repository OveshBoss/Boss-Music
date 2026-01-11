import os
from os import getenv
from dotenv import load_dotenv

if os.path.exists("local.env"):
    load_dotenv("local.env")

load_dotenv()

que = {}
admins = {}

# Mandatory Variables
SESSION_NAME = getenv("SESSION_NAME", "session")
BOT_TOKEN = getenv("BOT_TOKEN")
API_ID = int(getenv("API_ID"))
API_HASH = getenv("API_HASH")

# Bot Branding & Images
BOT_NAME = getenv("BOT_NAME", "ʙᴏss ᴍᴜsɪᴄ")
BG_IMAGE = getenv("BG_IMAGE", "https://telegra.ph/file/6790864f5fe27471bdc8d.png")
THUMB_IMG = getenv("THUMB_IMG", "https://telegra.ph/file/e9a4d6655e5ddf51f9160.jpg")
AUD_IMG = getenv("AUD_IMG", "https://telegra.ph/file/91034f175d41040d45b38.jpg")
QUE_IMG = getenv("QUE_IMG", "https://telegra.ph/file/c8a0e9c544c5ea689caf9.jpg")
BOT_USERNAME = getenv("BOT_USERNAME", "BossMusicSpotifyBot")
ASSISTANT_NAME = getenv("ASSISTANT_NAME", "OnlyBossManager")
GROUP_SUPPORT = getenv("GROUP_SUPPORT", "OnlyBossMoviesGroup")
UPDATES_CHANNEL = getenv("UPDATES_CHANNEL", "OveshBossOfficial")
OWNER_NAME = getenv("OWNER_NAME", "Ovesh_Boss")

# Permissions & IDs
PMPERMIT = getenv("PMPERMIT", None)
# Yahan 'OWNER_ID' variable name hai, aur '1416433622' default value
OWNER_ID = int(getenv("OWNER_ID", "1416433622")) 

# Database & Logs
# Direct URL dalna safe hai agar env variable nahi mil raha
DATABASE_URL = getenv("DATABASE_URL", "mongodb+srv://Ovesh:ovesh.boss@ovesh.95jpp8g.mongodb.net/?retryWrites=true&w=majority&appName=Ovesh")
LOG_CHANNEL = int(getenv("LOG_CHANNEL", "-1003166629808"))

# Settings
BROADCAST_AS_COPY = bool(getenv("BROADCAST_AS_COPY", False))
DURATION_LIMIT = int(getenv("DURATION_LIMIT", "60"))
COMMAND_PREFIXES = list(getenv("COMMAND_PREFIXES", "/ ! .").split())

# Sudo Users (Empty list handling)
sudo_users_raw = getenv("SUDO_USERS")
if sudo_users_raw:
    SUDO_USERS = list(map(int, sudo_users_raw.split()))
else:
    SUDO_USERS = [1416433622] # Default sudo user (Owner)

LANG = getenv("LANG", "id")

