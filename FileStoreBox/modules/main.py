from FileStoreBox import app, BOT_USERNAME
from pyrogram import filters
from FileStoreBox.core import script
from FileStoreBox.core import main_func
from FileStoreBox.core.mongo import toolsdb
from pyrogram.enums import MessageMediaType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup



@app.on_message((filters.document | filters.video | filters.forwarded) & filters.private)
async def watcher(_, message):
    try:
        user_id = message.from_user.id
        data = await toolsdb.get_data(user_id)
        
        if data and data.get("channel_id"):
            channel_id = data.get("channel_id")
            msg = await message.reply_text("<i>Processing...\nGenerating Link...</i>")
            file_caption = message.caption if message.caption else ""
            
            if message.video:
                file_id = message.video.file_id                  
            elif message.document:
                file_id = message.document.file_id
            else:
                await msg.edit_text("This media type is not supported!")
                return
            
            
            if data.get("api_url") and data.get("api_key"):
                encrypt_post_id = await main_func.base64_encrypt(f"{user_id}_{message.id}")
                bot_post_link = f"https://telegram.dog/{BOT_USERNAME}?start=FileBox_{encrypt_post_id}"
                short_post_link = await main_func.short_link(user_id, bot_post_link)
                buttons = [
                    [InlineKeyboardButton("🔗 Bot Link", url=bot_post_link)],
                    [InlineKeyboardButton("🏓 Shortener Link", url=short_post_link)],
                ]
            else:
                encrypt_post_id = await main_func.base64_encrypt(f"{user_id}_{message.id}")
                bot_post_link = f"https://telegram.dog/{BOT_USERNAME}?start=FileBox_{encrypt_post_id}"
                buttons = [[InlineKeyboardButton("🔗 Bot Link", url=bot_post_link)]]

            post = await _.send_cached_media(
                chat_id=channel_id,
                file_id=file_id,
                caption=file_caption,
                reply_markup=InlineKeyboardMarkup(buttons)
            )
            
            if data.get("api_url") and data.get("api_key"):
                encrypt_id = await main_func.base64_encrypt(f"{user_id}_{post.id}")
                bot_link = f"https://telegram.dog/{BOT_USERNAME}?start=FileBox_{encrypt_id}"
                short_link = await main_func.short_link(user_id, bot_link)
                buttons = [
                    [InlineKeyboardButton("🔗 Bot Link", url=bot_link)],
                    [InlineKeyboardButton("🏓 Shortener Link", url=short_link)],
                ]
            else:
                encrypt_id = await main_func.base64_encrypt(f"{user_id}_{post.id}")
                bot_link = f"https://telegram.dog/{BOT_USERNAME}?start=FileBox_{encrypt_id}"
                buttons = [[InlineKeyboardButton("🔗 Bot Link", url=bot_link)]]

            await message.reply_text(script.POST_TEXT, reply_markup=InlineKeyboardMarkup(buttons))
        else:
            await message.reply_text("**Channel ID not found or not configured!**\n\n<i>First, add your database channel then will you be able to store anything in the bot.</i>")
    except Exception as e:
        await msg.edit_text(f"**Error**: {e}")
        


