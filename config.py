from os import getenv


API_ID = int(getenv("API_ID", "26850449"))
API_HASH = getenv("API_HASH", "72a730c380e68095a8549ad7341b0608")
BOT_TOKEN = getenv("BOT_TOKEN","7513644126:AAFXZQ6MWA6WmsAgxzpMER3vB9Kr2UkwdxQ")
OWNER_ID = int(getenv("OWNER_ID", "6107581019"))
SUDO_USERS = list(map(int, getenv("SUDO_USERS", "6107581019 7091230649").split()))
MONGO_DB = getenv("MONGO_DB", "mongodb+srv://Extractor:ohUUMrBcLaCxlWZv@cluster0.nsjqx8b.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

CHANNEL_ID = int(getenv("CHANNEL_ID", "-1002405071668"))
PREMIUM_LOGS = int(getenv("PREMIUM_LOGS", "-1002091053529"))


