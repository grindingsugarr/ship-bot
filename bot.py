import random

from telegram import Update
from telegram.ext import (
    Application,
    MessageHandler,
    CommandHandler,
    ContextTypes,
    filters
)

from config import TOKEN
from database import update_user, get_users
from ship import choose_ship


async def track_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.message and update.message.from_user:
        update_user(
            update.effective_chat.id,
            update.message.from_user
        )


async def ship_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    users = get_users(update.effective_chat.id)

    result = choose_ship(users)

    if not result:
        await update.message.reply_text(
            "Member belum cukup untuk melakukan ship 😅"
        )
        return

    a, b = result

    name1 = a[2]
    name2 = b[2]

    chance = random.randint(50, 100)

    text = f"""
💘 SHIP OF THE MOMENT 💘

{name1} ❤️ {name2}

Compatibility:
🔥 {chance}%

Dipilih berdasarkan:
• Aktivitas grup
• Random matchmaking
"""

    await update.message.reply_text(text)


def main():

    app = Application.builder().token(TOKEN).build()

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            track_message
        )
    )

    app.add_handler(
        CommandHandler(
            "ship",
            ship_command
        )
    )

    print("Bot running...")

    app.run_polling()


if __name__ == "__main__":
    main()
