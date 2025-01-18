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
    sos = await app.ask(query.message.chat.id, text="<i>Give me your channel ID that you will use as a force channel.</i>")
    channel = sos.text
    await toolsdb.set_force_channel(query.from_user.id, channel)
    await query.message.reply_text("**✅ Successfully set your force channel ID, where users will be required to join before they can use the bot.**")

async def delete_force_channel(query):
    data = await toolsdb.get_data(query.from_user.id)  
    if data and data.get("channel_id"):
      await toolsdb.remove_force_channel(query.from_user.id)
      await query.answer("✅ Successfully removed your force channel ID.", show_alert=True)
    else:
      await query.answer("👀 You haven't set any force channel ID !!", show_alert=True)    
                                             
async def view_force_channel(query):
    data = await toolsdb.get_data(query.from_user.id)
    if data and data.get("force_channel"):
       force_channel = data.get("force_channel")
       await query.message.reply_text(f"**Here is your force channel ID, where users will be required to join before they can use the bot.**\n\n• `{force_channel}`")
    else:
       await query.answer("👀 You haven't set any force channel ID !!", show_alert=True)


# ---------------- Shortener ------------------- #

async def add_shortener(query):    
    aox = await app.ask(query.message.chat.id, text="**Send me your shortener api url**\n**Example**:- `https://modijiurl.com/api?`")
    api_url = aox.text
    kox = await app.ask(query.message.chat.id, text="**Now Send me your shortener api key**\n**Example**:- `818290dbdf8330715f3537ccdaddd064c5dc5530`")
    api_key = kox.text
    await toolsdb.set_shortener(query.from_user.id, api_url, api_key)
    await query.message.reply_text("**✅ Successfully set you shortener url and key.**")

async def delete_shortener(query):
    data = await db.get_data(query.from_user.id)  
    if data and data.get("api_url") and data.get("api_key"):
      await toolsdb.remove_shortener(query.from_user.id)
      await query.answer("✅ Successfully removed your shortener url and key.", show_alert=True)
    else:
      await query.answer("👀 You haven't set any shortener url and key !!", show_alert=True)    


async def view_shortener(query):
    data = await db.get_data(query.from_user.id)
    if data and data.get("api_url") and data.get("api_key"):
       api_key = data.get("api_key")
       api_url = data.get("api_url")
       await query.message.reply_text(f"**Here is your shortener url and key:**\n\n**Api Url**: `{api_url}`\n**Api Key**: `{api_key}`")
    else:
       await query.answer("👀 You haven't set any shortener url and key !!", show_alert=True)

