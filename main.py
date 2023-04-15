import datetime
import io
import os
import uuid

from dotenv import load_dotenv
from telegram import Update, InlineQueryResultCachedSticker
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, CallbackContext, InlineQueryHandler

import scrapper

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


async def send_photo_to_channel(update: Update, context: CallbackContext) -> None:
    """Send the message to the channel."""
    image_stream = scrapper.get_image_stream("https://epflplace.roundshot.com")
    if image_stream:
        bio = io.BytesIO()
        image_stream.save(bio, 'JPEG')
        bio.seek(0)
        timestamp_str = datetime.datetime.now().strftime("%Y-%m-%d %Hh%M")
        await context.bot.send_document(chat_id="@agora_epfl", document=bio, filename=timestamp_str + ".jpg")
    return


def main() -> None:
    """Start the bot."""
    print("Going live!")

    # Create application
    application = Application.builder().token(TOKEN).build()

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
