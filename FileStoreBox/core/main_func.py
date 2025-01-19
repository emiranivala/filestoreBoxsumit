import base64
import asyncio
import aiohttp
from config import HOST_URL
from pyrogram.enums import MessageMediaType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import UserNotParticipant
from FileStoreBox.core.mongo import toolsdb


async def base64_encrypt(input_string: str) -> str:
    encoded_bytes = base64.b64encode(input_string.encode('utf-8'))
    return encoded_bytes.decode('utf-8')

async def base64_decrypt(encoded_string: str) -> str:
    decoded_bytes = base64.b64decode(encoded_string.encode('utf-8'))
    return decoded_bytes.decode('utf-8')


async def must_join(_, message, user_id):
    data = await toolsdb.get_data(user_id)
    if data and data.get("force_channel"):
        force_channel = data.get("force_channel")
        if force_channel:
            invite_link = await _.create_chat_invite_link(force_channel)
            try:
                user = await _.get_chat_member(force_channel, message.from_user.id)
                if user.status == "kicked":
                    await message.reply_text("Sorry Sir, You are Banned from using me.")
                    return
            except UserNotParticipant:
                await message.reply_photo(
                    "https://telegra.ph/file/b7a933f423c153f866699.jpg", 
                    caption=script.FORCE_MSG.format(message.from_user.mention),
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("🤖 Join Update Channel", url=invite_link.invite_link)]
                    ])
                )
                return 1
    else:
        pass
        return 0



async def fetch_files(_, message):
    try:
        encode_data = message.text.split("_")
        parts = await base64_decrypt(encode_data)
        user_id = parts[1]
        id = parts[2]

        try:
            user = await app.get_users(user_id)
        except:
            pass
        joined = await must_join(_, message, user_id)
        if joined == 1:
            return

        data = await toolsdb.get_data(user_id)
        force_channel = data.get("force_channel") if data else None
        database_channel = data.get("channel_id") if data else None

        if database_channel is None:
            await message.reply_text("<i>Please contact {user.first_name}, the file provider. Maybe he has deleted or changed his database channel, which is why you are not getting the file.</i>")
            return

        if force_channel:
            invite_link = await _.create_chat_invite_link(force_channel)
            try:
                user = await _.get_chat_member(force_channel, message.from_user.id)
                if user.status == "kicked":
                    await message.reply_text("Sorry Sir, You are Banned from using me.")
                    return
            except Exception:
                await message.reply_photo(
                    "https://telegra.ph/file/b7a933f423c153f866699.jpg",
                    caption=script.FORCE_MSG.format(message.from_user.mention),
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("🤖 Join Update Channel", url=invite_link.invite_link)],
                        [InlineKeyboardButton("🔄 Try Again", callback_data=f"checksub#{id}")]
                    ])
                )
                return

        file = await _.get_messages(database_channel, int(id))
        file_caption = file.caption if file.caption else ""
        
        if file.media == "video":
            file_id = file.video.file_id
            title = file.video.file_name
        else:
            file_id = file.document.file_id
            title = file.document.file_name

        buttons = [[InlineKeyboardButton('Downloads', url=f"{HOST_URL}/{id}")]]

        await _.send_cached_media(
            chat_id=message.from_user.id,
            file_id=file_id,
            caption=file_caption,
            reply_markup=InlineKeyboardMarkup(buttons)
        )
        return
    except Exception as e:
        await message.reply_text(f"Error: `{str(e)}`")
        return




async def short_link(user_id, link):
    data = await toolsdb.get_data(user_id)
    if data and isinstance(data.get("api_url"), str) and isinstance(data.get("api_key"), str):
        api_url = data.get("api_url")
        api_key = data.get("api_key")

        if link.startswith("http://"):
            link = link.replace("http://", "https://")

        params = {'api': api_key, 'url': link}

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(api_url, params=params, ssl=False) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get("status") == "success":
                            return data.get('shortenedUrl')
                        else:
                            error_message = data.get('message', 'Unknown error occurred')
                            print(f"Error: {error_message}")
                    else:
                        print(f"HTTP Error: {response.status}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
    else:
        print("API URL or API Key is missing or invalid.")

    


