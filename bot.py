import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
import os
import sys
import asyncio

BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    raise ValueError("No BOT_TOKEN found in environment variables. Please set it before running the bot.")

ADMIN_ID = 7168112250  # Replace with your Telegram user ID

# Track user state
user_states = {}

# Set up logging
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_states[user_id] = "STARTED"

    logging.info("Received /start")
    await update.message.reply_text("🔄 Resetting keyboard...", reply_markup=ReplyKeyboardRemove())

    keyboard = [['Lets Deal']]
    reply_markup = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "👋 What's up! Tap the 'Lets Deal' button below to continue:",
        reply_markup=reply_markup
    )

# Main button/message handler
async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_input = update.message.text.strip().lower()
    logging.info(f"User input: {user_input}")

    full_name = f"{update.effective_user.first_name or ''} {update.effective_user.last_name or ''}".strip()
    username = update.effective_user.username
    display_name = full_name if full_name else f"@{username or 'UnknownUser'}"

    state = user_states.get(user_id)

    if "lets deal" in user_input:
        user_states[user_id] = "DEAL_SELECTED"

        keyboard = [
            ['I need your services'],
            ['I want to build a website'],
            ['I need your direct contact'],
            ['I want to discuss a deal with you'],
            ['Restart BOT']
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
        await update.message.reply_text(
            f"Hi, {display_name}, Welcome to Biggest Atom BOT, Powered by Khodex:\n"
            "A Programmer, Graphic Designer, Website Developer and Web Guru...\n\n"
            "What would you like to do?",
            reply_markup=reply_markup
        )
        return

    # If user hasn’t clicked “Lets Deal” yet
    if state != "DEAL_SELECTED":
        logging.info("Blocked message — user hasn't clicked 'Lets Deal' yet.")
        await update.message.reply_text(
            "❌ Please tap the 'Lets Deal' button first to proceed. Send /start if you don't see it."
        )
        return

    # --- Handle Options Below ---

    if "services" in user_input:
        await update.message.reply_text(
            "📩 Explain the service you need in full now and I will get back to you shortly, "
            "or email webdeveloper1972@gmail.com to keep it official and safe. "
            "I don't give out WhatsApp numbers directly — we'll switch if needed."
        )

    elif "build a website" in user_input:
        keyboard = [
            ['Courier Website'],
            ['Bitcoin Investment Website'],
            ['Tracking Website'],
            ['Auto-BOT'],
            ['Banking Website'],
            ['Blog Portal'],
            ['Business Website'],
            ['Company Website'],
            ['cPanel & Domains'],
            ['Restart BOT']
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
        await update.message.reply_text("🖥️ Choose the type of website you want to build:", reply_markup=reply_markup)

    elif "courier website" in user_input:
        await update.message.reply_text(
            "A courier website is an online platform designed for delivery services. It allows customers to schedule pickups, track shipments, and manage deliveries.\n\n"
            "Send your features in numbered format now and I will get back to you shortly, or email webdeveloper1972@gmail.com."
        )

    elif "bitcoin" in user_input:
        await update.message.reply_text(
            "A Bitcoin Investment Broker website allows users to invest Bitcoin with tracking, analytics, and guidance.\n\n"
            "Send your features in numbered format now and I will get back to you shortly or email: webdeveloper1972@gmail.com."
        )

    elif "tracking website" in user_input:
        await update.message.reply_text(
            "A tracking website is usually part of a courier system. If you mean another type, explain it to me now and I will get back to you shortly or email: webdeveloper1972@gmail.com."
        )

    elif "auto-bot" in user_input:
        await update.message.reply_text(
            "A bot automates tasks such as chatting or trading. Explain what you want and I’ll get back to you.\n\n"
            "Type it here now or email webdeveloper1972@gmail.com."
        )

    elif "banking" in user_input:
        await update.message.reply_text(
            "A custom banking website offers tailored financial services and branding for banks.\n\n"
            "Send your features in numbered format now and I will get back to you shortly or email webdeveloper1972@gmail.com."
        )

    elif "blog portal" in user_input:
        await update.message.reply_text(
            "A blog portal combines blog content with a hub of tools/resources.\n\n"
            "Send your WhatsApp number and features in numbered format now, or email webdeveloper1972@gmail.com."
        )

    elif "business website" in user_input:
        await update.message.reply_text(
            "A business website showcases your products, services, and contact info.\n\n"
            "Send your WhatsApp number and features in numbered format now, or email webdeveloper1972@gmail.com."
        )

    elif "company website" in user_input:
        await update.message.reply_text(
            "A company website is your digital face: team, mission, services, and more.\n\n"
            "Send your WhatsApp number and features in numbered format now, or email webdeveloper1972@gmail.com."
        )

    elif "cpanel" in user_input or "domain" in user_input:
        await update.message.reply_text(
            "We can set up cPanel and domains along with your website project.\n\n"
            "Send the domain details and required features now or email webdeveloper1972@gmail.com."
        )

    elif "restart bot" in user_input:
        user_states[user_id] = "STARTED"
        keyboard = [['Lets Deal']]
        reply_markup = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
        await update.message.reply_text("🔁 Bot restarted. Tap 'Lets Deal' to begin again.", reply_markup=reply_markup)

    else:
        # Unrecognized input (after "Lets Deal") — forward to admin
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"📩 Message from {display_name} (@{username or 'unknown'}):\n\n{update.message.text}"
        )
        await update.message.reply_text("✅ Perfect, Your message has been received. I will get back to you shortly.")

def main():
    # Windows event loop fix
    if sys.platform.startswith("win"):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    try:
        app = ApplicationBuilder().token(BOT_TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_buttons))

        print("✅ Bot is running...")
        app.run_polling()
    except Exception as e:
        print("🚨 Error during startup:", e)
        raise

if __name__ == "__main__":
    main()