from config import MONGO_DB
from motor.motor_asyncio import AsyncIOMotorClient as MongoCli


mongo = MongoCli(MONGO_DB)
db = mongo.users_tools
db = db.tools_db

# ----------------------------------------------------------- #

async def get_data(user_id):
    lmao = await db.find_one({"_id": user_id})
    return lmao


async def set_channel(user_id, chat_id):
    data = await get_data(user_id)
    if data and data.get("_id"):
        await db.update_one({"_id": user_id}, {"$set": {"channel_id": chat_id}})
    else:
        await db.insert_one({"_id": user_id, "channel_id": chat_id})


async def set_force_channel(user_id, chat_id):
    data = await get_data(user_id)
    if data and data.get("_id"):
        await db.update_one({"_id": user_id}, {"$set": {"force_channel": chat_id}})
    else:
        await db.insert_one({"_id": user_id, "force_channel": chat_id})


async def set_shortener(user_id, api_url, api_key):
    data = await get_data(user_id)
    if data and data.get("_id"):
        await db.update_one({"_id": user_id}, {"$set": {"api_url": api_url, "api_key": api_key}})
    else:
        await db.insert_one({"_id": user_id, "api_url": api_url, "api_key": api_key})


# ----------------------------------------------------------- #
        
async def remove_channel(user_id):
    await db.update_one({"_id": user_id}, {"$set": {"channel_id": None}})

async def remove_force_channel(user_id):
    await db.update_one({"_id": user_id}, {"$set": {"force_channel": None}})

async def remove_shortener(user_id):
    await db.update_one({"_id": user_id}, {"$set": {"api_url": None, "api_key": None}})


# ----------------------------------------------------------- #


