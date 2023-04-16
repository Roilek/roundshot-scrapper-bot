import argparse
import asyncio
import datetime
import io
import os
import uuid

import pytz as pytz
import telegram
from dotenv import load_dotenv
from telegram import Update, InlineQueryResultCachedSticker
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, CallbackContext, InlineQueryHandler

import scrapper

bot: telegram.Bot = None

# Load the environment variables

load_dotenv()

TOKEN = os.getenv("TOKEN")
PORT = int(os.getenv('PORT', 5000))
HEROKU_PATH = os.getenv('HEROKU_PATH')


async def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_text("Yo la zone")
    return


async def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text('Contactez @eliorpap pour plus d\'infos !')
    return


async def dump(update: Update, context: CallbackContext) -> None:
    """Dump the update object."""
    await update.message.reply_text(f"```{update}```", parse_mode=ParseMode.MARKDOWN_V2)
    return


async def send_photo_to_channel(update: Update = None, context: CallbackContext = None) -> None:
    """Send the message to the channel."""
    # TODO extract constants
    image_stream = scrapper.get_image_stream("https://epflplace.roundshot.com")
    if image_stream:
        bio = io.BytesIO()
        image_stream.save(bio, 'JPEG')
        bio.seek(0)
        # Get my timezone
        tz = pytz.timezone('Europe/Zurich')
        timestamp_str = datetime.datetime.now(tz).strftime("%Y-%m-%d %Hh%M")
        await bot.send_document(chat_id="@agora_epfl", document=bio, filename=timestamp_str + ".jpg")
    return


def main() -> None:
    """Start the bot."""
    # Create application
    application = Application.builder().token(TOKEN).build()
    global bot
    bot = application.bot

    # Parse the arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("function",
                        nargs='?',
                        help="The function to execute",
                        choices=["send_photo_to_channel"])
    args = parser.parse_args()

    # If a function is specified, execute it and exit
    if args.function == "send_photo_to_channel":
        asyncio.run(send_photo_to_channel())
        return

    print("Going live!")

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("dump", dump))
    application.add_handler(CommandHandler("pic", send_photo_to_channel))

    # Start the Bot
    print("Bot starting...")
    if os.environ.get('ENV') == 'DEV':
        application.run_polling()
    elif os.environ.get('ENV') == 'PROD':
        application.run_webhook(listen="0.0.0.0",
                                port=int(PORT),
                                webhook_url=HEROKU_PATH)
    return


if __name__ == '__main__':
    main()
