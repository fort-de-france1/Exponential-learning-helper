import os
from dotenv import load_dotenv
import time
import datetime

from django.core.management import BaseCommand
from exp_bot_app.models import Remind

from exp_bot_app.management.commands.telegram_client import TelegramClient
from logging import getLogger, StreamHandler

logger = getLogger(__name__)
logger.addHandler(StreamHandler())
logger.setLevel("INFO")
load_dotenv()


class Command(BaseCommand):
    help = "Reminder client"

    def handle(self, *args, **options):
        start_time = datetime.datetime.strptime(os.getenv("FROM_TIME"), "%H:%M").time()
        end_time = datetime.datetime.strptime(os.getenv("TO_TIME"), "%H:%M").time()
        telegram_client = TelegramClient(token=os.getenv("TOKEN"), base_url=os.getenv("BASE_URL"))
        reminder = Reminder(telegram_client=telegram_client)
        while True:
            now_time = datetime.datetime.now().time()
            if start_time <= now_time <= end_time:
                reminder()
                time.sleep(5)
                logger.info("sleep 2")
            else:
                time.sleep(10)
                logger.info("sleep 10")


class Reminder:
    GET_TASKS = Remind.objects.filter(date_remind=datetime.date.today())

    def __init__(self, telegram_client: TelegramClient):
        self.telegram_client = telegram_client

    def notify(self, all_reminders: list):
        for rem in Remind.objects.filter(date_remind=datetime.date.today()):
            print(rem.profile)
            print(rem.date_remind)
            res = self.telegram_client.post(method="sendMessage",
                                            params={"text": f"Notification!\n"
                                                            f"You must repeat this:\n\n"
                                                            f"Title: {rem.title}\n"
                                                            f"Description: {rem.content}\n\n"
                                                            f"\nremind {rem.date_remind}\n"
                                                            f"Send /done to mark repeat",

                                                    "chat_id": rem.profile.telegram_id, }, )
        # logger.info(res)

    def prepare(self):
        all_reminders = self.GET_TASKS
        if all_reminders:
            self.notify(all_reminders=all_reminders)

    def __call__(self, *args, **kwargs):
        self.prepare()
