from pyrogram import filters
from FileStoreBox import app
from FileStoreBox.core import script
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup




button = InlineKeyboardMarkup([[
          InlineKeyboardButton("Tool Box", callback_data="tools_")                
       ]])



@app.on_message(filters.command("start") & filters.private)
async def start(_, message):        
    if message.text.startswith("/start FileBox"):
        pass
        return 
        
    elif message.text.startswith("/start BatchBox"):
        reffer_id = message.text.split("_")[1]
        pass
        return 
    else:
        await message.reply_photo(
            photo="https://envs.sh/Hpz.jpg",
            caption=script.START_TEXT.format(message.from_user.first_name),
            reply_markup=button
        )

  

buttons = InlineKeyboardMarkup([
      [
          InlineKeyboardButton("Database", callback_data="database_"),          ,
          InlineKeyboardButton("Force", callback_data="force_"),
          InlineKeyboardButton("Shortener", callback_data="shortener_")
      ],[   
          InlineKeyboardButton("🔙 Back", callback_data="home_") 
      ]])





@app.on_callback_query()
async def handle_callback(_, query):
    if query.data == "home_":
        await query.message.edit_text(
            script.START_TXT.format(query.from_user.mention),
            reply_markup=button
        )
    elif query.data == "tools_":
        await query.message.edit_text(
            script.TOOLS_TEXT,
            reply_markup=buttons
        )
    elif query.data == "database_":
        await query.message.edit_text(
            script.DATABASE_TEXT,
            reply_markup=buttons1
        )
    elif query.data == "force_":
        await query.message.edit_text(
            script.FORCE_TEXT,
            reply_markup=buttons2
        )
    elif query.data == "shortener_":
        await query.message.edit_text(
            script.SHORTENER_TEXT,
            reply_markup=buttons3
        )
    elif query.data == "maintainer_":
        await query.answer(
            "sᴏᴏɴ.... \nʙᴏᴛ ᴜɴᴅᴇʀ ɪɴ ᴍᴀɪɴᴛᴀɪɴᴀɴᴄᴇ",
            show_alert=True
        )
    elif query.data == "close_data":
        try:
            await query.message.delete()
            if query.message.reply_to_message:
                await query.message.reply_to_message.delete()
        except Exception as e:
            print(f"Error deleting messages: {e}")


                  
