from pyrogram import filters
from FileStoreBox import app
from FileStoreBox.core import script
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup




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

  
