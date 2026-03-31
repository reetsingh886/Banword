from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from pyrogram.enums import ChatType
from config import OWNER_ID, BOT_USERNAME
from Banword import Banword as app
from Banword.helper.database import add_user, add_chat

START_IMG = "https://files.catbox.moe/v1h6yh.jpg"

def get_start_caption(user):
    return f"""
**ʜᴇʏ** {user.mention} 🥀

🤖 I am a **Banword Remover Bot**.
I delete messages with Banword and restrict users who have Banword .

🚫 I also delete messages with **Banword**.
"""

START_BUTTONS = InlineKeyboardMarkup([
    [InlineKeyboardButton("• ᴀᴅᴅ ᴍᴇ •", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")],
    [InlineKeyboardButton("• ʜᴇʟᴘ ᴀɴᴅ ᴄᴏᴍᴍᴀɴᴅ •", callback_data="show_help")],
    [
        InlineKeyboardButton("• ʟᴏɢs •", url="https://t.me/BotsSupport_36"),
        InlineKeyboardButton("• ᴜᴘᴅᴀᴛᴇ •", url="https://t.me/BOTxBOOSTER")
    ],
    [InlineKeyboardButton("🥀 ᴅᴇᴠᴇʟᴏᴩᴇʀ 🥀", url="https://t.me/iamthakur007")]
])

PRIVATE_START_BUTTON = InlineKeyboardMarkup([
    [InlineKeyboardButton("• ᴘʀɪᴠᴀᴛᴇ ꜱᴛᴀʀᴛ •", url=f"https://t.me/{BOT_USERNAME}?start=help")]
])

@app.on_message(filters.command("start") & (filters.private | filters.group))
async def start_command(_, message: Message):
    user = message.from_user
    chat = message.chat

    await add_user(user.id)
    if chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
        await add_chat(chat.id)

    if chat.type == ChatType.PRIVATE:
        await message.reply_photo(
            photo=START_IMG,
            caption=get_start_caption(user),
            has_spoiler=True,
            reply_markup=START_BUTTONS
        )
    else:
        await message.reply_text(
            f"**ʜᴇʏ {user.mention}, ᴛʜᴀɴᴋꜱ ꜰᴏʀ ᴀᴅᴅɪɴɢ ᴍᴇ!**",
            reply_markup=PRIVATE_START_BUTTON
        )

@app.on_callback_query(filters.regex("^back_to_start$"))
async def back_to_start(_, query: CallbackQuery):
    user = query.from_user
    chat_id = query.message.chat.id

    await query.message.delete() 

    await app.send_photo(
        chat_id=chat_id,
        photo=START_IMG,
        caption=get_start_caption(user),
        has_spoiler=True,
        reply_markup=START_BUTTONS
    )
    
