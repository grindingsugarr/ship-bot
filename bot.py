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

    a, b, compatibility = result

    username1 = f"@{a[1]}" if a[1] else a[2]
    username2 = f"@{b[1]}" if b[1] else b[2]

    text = f"""
💘 SHIP OF THE MOMENT 💘

<a href="tg://user?id={a[0]}">{username1}</a> ❤️ <a href="tg://user?id={b[0]}">{username2}</a>

Compatibility:
🔥 {compatibility}%

📊 Analisis:
• Aktivitas grup tinggi
• Sering muncul dalam percakapan
• Belum pernah dipasangkan sebelumnya

✨ Match reason:
"Sering berinteraksi dalam grup"
"""

    await update.message.reply_text(
              text,
              parse_mode="HTML",
    disable_web_page_preview=True
)

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
