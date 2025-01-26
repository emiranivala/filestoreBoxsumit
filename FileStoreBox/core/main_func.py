import base64
import asyncio
import aiohttp
from FileStoreBox.core import script
from pyrogram.enums import MessageMediaType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import UserNotParticipant
from FileStoreBox.core.mongo import toolsdb




async def base64_encrypt(input_string: str) -> str:
    encoded_bytes = base64.b64encode(input_string.encode('utf-8'))
    return encoded_bytes.decode('utf-8').rstrip('=')

async def base64_decrypt(encoded_string: str) -> str:
    padding_needed = len(encoded_string) % 4
    if padding_needed:
        encoded_string += '=' * (4 - padding_needed)
    decoded_bytes = base64.b64decode(encoded_string.encode('utf-8'))
    return decoded_bytes.decode('utf-8')


async def must_join(_, message, user_id, sender_id, name):
    data = await toolsdb.get_data(user_id)
    if data and data.get("force_channel"):
        force_channel = data.get("force_channel")
        if force_channel:
            invite_link = await _.create_chat_invite_link(force_channel)
            try:
                user = await _.get_chat_member(force_channel, sender_id)
                if user.status == "kicked":
                    await message.reply_text("Sorry Sir, You are Banned from using me.")
                    return
            except UserNotParticipant:
                await message.reply_photo(
                    "https://telegra.ph/file/b7a933f423c153f866699.jpg", 
                    caption=script.FORCE_MSG.format(name),
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("🤖 Join Update Channel", url=invite_link.invite_link)]
                    ])
                )
                return 1
    else:
        pass
        return 0



async def fetch_files(_, message, encrypt_mode=True, query=None):
    try:
        if encrypt_mode:
            name = message.from_user.mention
            sender_id = message.from_user.id
            encode_data = message.text.split("_")
            decrypt_data = await base64_decrypt(encode_data[1])
            parts = decrypt_data.split("_")
            user_id = parts[0]
            id = parts[1]
        else:
            name = query.from_user.mention
            sender_id = query.from_user.id
            task = query.data.split("#")[1]
            parts = task.split("_")
            user_id = parts[0]
            id = parts[1]
            
    
        try:
            user = await app.get_users(user_id)
        except:
            pass

        joined = await must_join(_, message, user_id, sender_id, name)
        if joined == 1:
            return

        data = await toolsdb.get_data(int(user_id))
        force_channel = data.get("force_channel")
        database_channel = data.get("channel_id")

        if database_channel is None:
            await message.reply_text(
                f"<i>Please contact {user.mention}, the file provider. Maybe he has deleted or changed his database channel, which is why you are not getting the file.</i>"
            )
            return

        if force_channel:
            invite_link = await _.create_chat_invite_link(force_channel)
            try:
                user = await _.get_chat_member(force_channel, sender_id)
                if user.status == "kicked":
                    await message.reply_text("Sorry Sir, You are Banned from using me.")
                    return
            except Exception:
                await message.reply_photo(
                    "https://telegra.ph/file/b7a933f423c153f866699.jpg",
                    caption=script.FORCE_MSG.format(name),
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("🤖 Join Update Channel", url=invite_link.invite_link)],
                        [InlineKeyboardButton("🔄 Try Again", callback_data=f"checksub#{user_id}_{id}")]
                    ])
                )
                return

        file = await _.get_messages(database_channel, int(id))
        file_caption = file.caption if file.caption else ""

        file_id = None  
        if file.media == MessageMediaType.VIDEO:
            file_id = file.video.file_id
        elif file.media == MessageMediaType.DOCUMENT:
            file_id = file.document.file_id

        if not file_id:
            await message.reply_text("<i>Unsupported media type. Please contact the provider for help.</i>")
            return

        await _.send_cached_media(
            chat_id=sender_id,
            file_id=file_id,
            caption=file_caption
        )
        return
    except Exception as e:
        await message.reply_text(f"Error: `{str(e)}`")
        return



async def batch_files(_, message, encrypt_mode=True, query=None):
    try:
        if encrypt_mode:
            name = message.from_user.mention
            sender_id = message.from_user.id
            encode_data = message.text.split("_")
            decrypt_data = await base64_decrypt(encode_data[1])
            parts = decrypt_data.split("_")
            user_id = parts[0]
            start_id = parts[1]
            last_id = parts[2]
        else:
            name = query.from_user.mention
            sender_id = query.from_user.id
            task = query.data.split("#")[1]
            parts = task.split("_")
            user_id = parts[0]
            start_id = parts[1]
            last_id = parts[2]
            

        try:
            user = await app.get_users(user_id)
        except Exception:
            user = None

        joined = await must_join(_, message, user_id, sender_id, name)
        if joined == 1:
            return

        data = await toolsdb.get_data(int(user_id))
        force_channel = data.get("force_channel")
        database_channel = data.get("channel_id")

        if database_channel is None:
            await message.reply_text(
                f"<i>Please contact {user.mention if user else 'the file provider'}. "
                "The database channel might be deleted or changed, which is why you cannot access the file.</i>"
            )
            return

        if force_channel:
            invite_link = await _.create_chat_invite_link(force_channel)
            try:
                user_status = await _.get_chat_member(force_channel, sender_id)
                if user_status.status == "kicked":
                    await message.reply_text("Sorry Sir, You are Banned from using me.")
                    return
            except Exception:
                await message.reply_photo(
                    "https://telegra.ph/file/b7a933f423c153f866699.jpg",
                    caption=script.FORCE_MSG.format(name),
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("🤖 Join Update Channel", url=invite_link.invite_link)],
                        [InlineKeyboardButton("🔄 Try Again", callback_data=f"batchSub#{user_id}_{start_id}_{last_id}")]
                    ])
                )
                return

        for id in range(int(start_id), int(last_id) + 1):
            try:
                file = await _.get_messages(database_channel, int(id))
                file_caption = file.caption if file.caption else ""

                file_id = None
                if file.media == MessageMediaType.VIDEO:
                    file_id = file.video.file_id
                elif file.media == MessageMediaType.DOCUMENT:
                    file_id = file.document.file_id

                if not file_id:
                    await message.reply_text("<i>Unsupported media type. Please contact the provider for help.</i>")
                    continue

                await _.send_cached_media(
                    chat_id=sender_id,
                    file_id=file_id,
                    caption=file_caption                    
                )
                await asyncio.sleep(0.8)
            except Exception as file_error:
                print(f"Failed to process file ID {id}: {file_error}")
                continue
    except Exception as e:
        await message.reply_text(f"Error: `{str(e)}`")
        return



