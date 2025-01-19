from FileStoreBox import app
from pyrogram import filters
from FileStoreBox.core import script
from FileStoreBox.core import main_func
fron FileStoreBox.core.mongo import toolsdb
from pyrogram.enums import MessageMediaType


@app.on_message((filters.document | filters.video | filters.forward) & filters.private)
async def watcher(_, message):
    try:
        user_id = message.from_user.id
        data = await toolsdb.get_data(user_id)
        if data and data.get("channel_id"):
          channel_id = data.get("channel_id")
          
          msg = await message.reply_text("<i>Processing...\nGenerating Link...</i>")
          file_caption = message.caption if message.caption else ""
      
          if message.media == MessageMediaType.VIDEO:
             file_id = message.video.file_id                  
          elif message.media == MessageMediaType.DOCUMENT:
             file_id = message.document.file_id
          else:
             await msg.edit_text("Not Support this media !!")
             return
            
          if data and data.get("api_url") and data.get("api_key"):
            encrypt_post_id = f"{user_id}_{message.id}"
            bot_post_link = f"https://telegram.dog/{BOT_USERBAME}?start=FileBox_{encrypt_post_id}" 
            short_post_link = await main_func.short_link(user_id, bot_link)
            buttons = [
                    [InlineKeyboardButton("🔗 Bot Link", url=bot_post_link)],
                    [InlineKeyboardButton("🏓 Shortener Link", url=short_post_link)],
                      ]
          else: 
            buttons = [[InlineKeyboardButton("🔗 Bot Link", url=bot_post_link)]]
            
          msg_id = await _.send_cached_media(
            chat_id=channel_id,
            file_id=file_id,
            caption=file_caption,
            reply_markup=InlineKeyboardMarkup(buttons)
          )
          if data and data.get("api_url") and data.get("api_key"):
            encrypt_id = f"{user_id}_{msg_id}"
            bot_link = f"https://telegram.dog/{BOT_USERBAME}?start=FileBox_{encrypt_post_id}" 
            short_link = await main_func.short_link(user_id, bot_link)
            buttons = [
                    [InlineKeyboardButton("🔗 Bot Link", url=bot_link)],
                    [InlineKeyboardButton("🏓 Shortener Link", url=short_link)],
                      ]
          else: 
            buttons = [[InlineKeyboardButton("🔗 Bot Link", url=bot_link)]]
          await message.reply_text(script.POST_TEXT, reply_markup=buttons)
            
     except:
       await msg.edit_text("something went wrong!! ")
            
