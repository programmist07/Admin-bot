from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, CallbackQueryHandler, filters


ADMIN_ID = ("number")
CHANNEL_ID = ("number")

USER_DATA_FILE = 'user_data.txt'

def save_user_data(user_id, username):
    with open(USER_DATA_FILE, 'a') as file:
        file.write(f"{user_id},{username}\n")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    save_user_data(user.id, user.username)
    await update.message.reply_text(
        f"Welcome, {user.first_name}! Your data has been saved.",
        reply_markup=ReplyKeyboardMarkup([['Help', 'About']], resize_keyboard=True)
    )

    await context.bot.send_message(
        chat_id=CHANNEL_ID,
        text=f"New user: {user.first_name} (@{user.username}), ID: {user.id}"
    )

async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id == ADMIN_ID:
        with open(USER_DATA_FILE, 'r') as file:
            data = file.read()
        await update.message.reply_text(f"User Data:\n{data}")
    else:
        await update.message.reply_text("Access denied!")

async def inline_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("You clicked an inline button!")

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("I received your message!")

app = ApplicationBuilder().token("Token here").build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("admin", admin))
app.add_handler(CallbackQueryHandler(inline_handler))  
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))  

app.run_polling()
