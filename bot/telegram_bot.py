from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
import requests
from django.conf import settings

BOT_TOKEN = "7611352526:AAHFz0r0X_6kV9Uv5EyN-kx-WE5DuBXa3Vk"
url = "http://127.0.0.1:8000/temperature/get-temperature-data/"
# Command to fetch temperature data
# Command to fetch temperature data
async def get_temperature(update: Update, context: CallbackContext):
    try:
        # Call your temperature endpoint
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        print(f"Response Text: {response.text}")
        if response.status_code == 200:
            data = response.json()["data"]
            if not data:
                await update.message.reply_text("No temperature data available.")
                return

            # Format the response
            message = "Last 5 Temperature Records:\n"
            for entry in data[:5]:
                message += f"{entry['time']}: {entry['value']} °C\n"
            await update.message.reply_text(message)
        else:
            await update.message.reply_text("Failed to fetch temperature data.")
    except Exception as e:
        await update.message.reply_text(f"An error occurred: {str(e)}")

# Start the bot
def start_bot():
    # Create the application
    application = Application.builder().token(BOT_TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("temperature", get_temperature))

    # Start the bot
    application.run_polling()