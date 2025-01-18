from FileStoreBox import app
from FileStoreBox.core.mongo import toolsdb

# ---------------- Database-Channel ------------------- #

async def add_channel(query):    
    sto = await app.ask(query.message.chat.id, text="<i>Give me your channel ID that you will use as a database.</i>")
    channel = sto.text
    await toolsdb.set_channel(query.from_user.id, channel)
    await query.message.reply_text("**✅ Successfully set your channel ID as a database where your media will be stored.**")

async def delete_channel(query):
    data = await toolsdb.get_data(query.from_user.id)  
    if data and data.get("channel_id"):
      await toolsdb.remove_channel(query.from_user.id)
      await query.answer("✅ Successfully removed your channel ID as a database.", show_alert=True)
    else:
      await query.answer("👀 You haven't set any channel ID !!", show_alert=True)    


async def view_channel(query):
    data = await toolsdb.get_data(query.from_user.id)
    if data and data.get("channel_id"):
       channel_id = data.get("channel_id")
       await query.message.reply_text(f"**Here is your channel ID that you added as a database. All your data will be stored in this channel.**\n\n• `{channel_id}`")
    else:
       await query.answer("👀 You haven't set any channel ID !!", show_alert=True)

# ---------------- Force-Channel ------------------- #
async def add_force_channel(query):    
    sos = await app.ask(query.message.chat.id, text="Give me a caption to set.")
    channel = sos.text
    await toolsdb.set_force_channel(query.from_user.id, channel)
    await query.message.reply_text("✅ Your caption has been successfully set.")

async def delete_force_channel(query):
    data = await toolsdb.get_data(query.from_user.id)  
    if data and data.get("channel_id"):
      await toolsdb.remove_force_channel(query.from_user.id)
      await query.answer("☘️ Your session has been successfully deleted.", show_alert=True)
    else:
      await query.answer("👀 You haven't set any session !!", show_alert=True)    
                                             
async def view_force_channel(query):
    data = await toolsdb.get_data(query.from_user.id)
    if data and data.get("force_channel"):
       force_channel = data.get("force_channel")
       await query.message.reply_text(f"**Here is your string session**\n\n`{string_session}`")
    else:
       await query.answer("👀 You haven't set any session !!", show_alert=True)


# ---------------- Shortener ------------------- #

async def add_shortener(query):    
    aox = await app.ask(query.message.chat.id, text="Send me the text you want to replace.")
    api_url = aox.text
    kox = await app.ask(query.message.chat.id, text="Send me the text you'd like to have replaced.")
    api_key = kox.text
    await toolsdb.set_shortener(query.from_user.id, api_url, api_key)
    await query.message.reply_text("✅ Your replace caption has been successfully set.")

async def delete_shortener(query):
    data = await db.get_data(query.from_user.id)  
    if data and data.get("api_url") and data.get("api_key"):
      await toolsdb.remove_shortener(query.from_user.id)
      await query.answer("☘️ Your replace caption has been successfully deleted.", show_alert=True)
    else:
      await query.answer("👀 You haven't set any replace caption !!", show_alert=True)    


async def view_shortener(query):
    data = await db.get_data(query.from_user.id)
    if data and data.get("api_url") and data.get("api_key"):
       replace = data.get("api_key")
       to_replace = data.get("api_url")
       await query.message.reply_text(f"**Your replace text:** `{replace}`\n\nYour to replace text: `{to_replace}`")
    else:
       await query.answer("👀 You haven't set any caption !!", show_alert=True)

