from django.core.management.base import BaseCommand
from bot.telegram_bot import start_bot

class Command(BaseCommand):
    help = "Starts the Telegram bot"

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting Telegram bot...")
        start_bot()
