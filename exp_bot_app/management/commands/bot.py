import os
from dotenv import load_dotenv
import datetime

from django.core.management.base import BaseCommand
from exp_bot_app.models import Remind, Profile, CurrentRemind

from .telegram_client import TelegramClient
import telebot
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from logging import getLogger, StreamHandler

load_dotenv()
logger = getLogger(__name__)
logger.addHandler(StreamHandler())
logger.setLevel("INFO")


def formula(day: int):
    return 2 * day + 1


class MyBot(telebot.TeleBot):
    def __init__(self, telegram_client: TelegramClient, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.telegram_client = telegram_client


telegram_client = TelegramClient(token=os.getenv("TOKEN"), base_url=os.getenv("BASE_URL"))

bot_client = MyBot(token=os.getenv("TOKEN"), telegram_client=telegram_client)


def create_err_msg(err: Exception) -> str:
    pass


# Send /create to add new.
# Send /show to view all your reminders.
class Command(BaseCommand):
    help = "Telegram bot"

    def handle(self, *args, **options):
        while True:
            try:
                bot_client.polling()
            except Exception as err:
                # TODO create func for build error message

                bot_client.telegram_client.post(method="sendMessage",
                                                params={"text": f"{datetime.datetime.now()}\n"
                                                                f"{err.__class__}\n"
                                                                f"{err}",
                                                        "chat_id": 1147257669})
                logger.error(err)


def get_y_o_r_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Yes", callback_data="Yes"),
               InlineKeyboardButton("No", callback_data="No"))
    return markup


# Registration new user
@bot_client.message_handler(commands=["start"])
def start(message: Message):
    chat_id = message.chat.id
    name = message.from_user.username
    Profile.objects.update_or_create(
        telegram_id=chat_id,
        defaults={
            "name": message.from_user.username,
        }
    )
    bot_client.reply_to(message, f"Hello {name}, let's create new reminders.\n\n"
                                 f"Send /create to add new.")


# Add new remind into database with pars string
def create_remind(message: Message):
    """

    :param message:
    - Create new user remind.

    """
    try:
        telegram_id = Profile.objects.get(telegram_id=message.chat.id)
    except  Exception:
        bot_client.send_message(chat_id=message.chat.id, text="Something wrong")
        return
    title = message.text.split("\n")[0]
    content = message.text.split("\n")[1:]
    content = " ".join(content).strip()
    if Remind.objects.create(
            profile_id=telegram_id.id,
            title=title,
            content=content,
            day_repeat=formula(1),
            date_remind=datetime.date.today() + datetime.timedelta(days=formula(1))

    ):
        bot_client.send_message(chat_id=message.chat.id, text="Remind created.\n\n"
                                                              "Send /show to view all your reminders.")
    else:
        bot_client.send_message(chat_id=message.chat.id, text="Something wrong, try again.\n\n /create.")


@bot_client.message_handler(commands=["create"])
def create(message: Message):
    """

    :param message:
    :command: /create
    - This method send instruction for user input
    and redirect to create_remind.
    """
    bot_client.send_message(chat_id=message.chat.id,
                            text=f"OK. Send me a <b>title</b> and <b>description</b> (optional)"
                                 f" Please use this format:\n\n"
                                 f"Title\n\nDescription", parse_mode="HTML")
    bot_client.register_next_step_handler(message, callback=create_remind)


@bot_client.callback_query_handler(func=lambda call: "Done" in call.data)
def change_is_repeat_status(call):
    id_rem = call.data[4:]
    rem = Remind.objects.get(id=id_rem)
    rem.day_repeat = formula(rem.day_repeat)
    rem.date_remind = datetime.date.today() + datetime.timedelta(days=rem.day_repeat)
    rem.save()
    # TODO: Add count days for next repeat in "text"
    bot_client.answer_callback_query(call.id, text=f"Greate! Repeat after {rem.day_repeat} - days.",
                                     show_alert=True)
    bot_client.delete_message(call.message.chat.id, call.message.id)


@bot_client.message_handler(commands=["done"])
def done(message: Message):
    usr = Profile.objects.get(telegram_id=message.chat.id)
    today_reminders = Remind.objects.filter(profile_id=usr.id).filter(date_remind=datetime.date.today())
    if today_reminders:
        for rem in today_reminders:
            markup = InlineKeyboardMarkup()
            markup.row_width = 1
            markup.add(InlineKeyboardButton("Done", callback_data=f"Done{rem.id}"))
            bot_client.send_message(chat_id=message.chat.id,
                                    text=f"<b>Title:</b> {rem.title}\n"
                                         f"<b>Description:</b> {rem.content}",
                                    reply_markup=markup,
                                    parse_mode="HTML")
    else:
        bot_client.send_message(chat_id=message.chat.id,
                                text=f"<b>No tasks for repeat.</b>",
                                parse_mode="HTML")


@bot_client.message_handler(commands=["show"])
def show(message: Message):
    usr = Profile.objects.get(telegram_id=message.chat.id)
    data = Remind.objects.filter(profile_id=usr.id)

    if data:
        for rem in data:
            markup = InlineKeyboardMarkup()
            markup.row_width = 1
            markup.add(InlineKeyboardButton("Edit", callback_data=f"Edit{rem.id}"))
            bot_client.send_message(chat_id=message.chat.id,
                                    text=f"<b>Title: </b>\n{rem}\n\n"
                                         f"<b>Description:</b>\n{rem.content}", reply_markup=markup,
                                    parse_mode="HTML")

    else:
        bot_client.send_message(chat_id=message.chat.id,
                                text=f"You don't have reminds.\n\n"
                                     f"Send /create to add new.")


@bot_client.callback_query_handler(func=lambda call: call.data == "Yes" or call.data == "No")
def yes_or_no(call):
    if call.data == "Yes":
        usr = Profile.objects.get(telegram_id=call.message.chat.id)
        rem_id = CurrentRemind.objects.get(telegram_id=usr.id)
        Remind.objects.filter(id=rem_id.rem_id).delete()
        bot_client.answer_callback_query(call.id, text="Remind deleted", show_alert=True)
        bot_client.delete_message(call.message.chat.id, call.message.id)
        return
    elif call.data == "No":
        bot_client.answer_callback_query(call.id, text="Cansel", show_alert=True)
        bot_client.delete_message(call.message.chat.id, call.message.id)
        return


@bot_client.callback_query_handler(func=lambda call: "Edit" in call.data)
def callback_query(call):
    usr = Profile.objects.get(telegram_id=call.message.chat.id)
    id_rem = call.data[4:]
    cur_rem, created = CurrentRemind.objects.update_or_create(
        telegram_id=usr.id,
        defaults={"rem_id": id_rem}
    )
    rem = Remind.objects.get(id=cur_rem.rem_id)

    bot_client.send_message(call.message.chat.id, text=f"<b>Edit mode</b>\n\n"
                                                       f"<b>Title:</b> {rem.title}\n"
                                                       f"<b>Description:</b> {rem.content}\n\n"
                                                       f"Send me a <b>title</b> and <b>description</b> (optional) "
                                                       f"Please use this format:\n\n"
                                                       f"<b>Title</b>\n\n<b>Description</b>\n\n"
                                                       f"To <b>cansel Editing</b> send /cansel\n"
                                                       f"To <b>Delete</b> this message send /delete", parse_mode="HTML")
    message_id = call.message.id
    print(message_id)
    bot_client.register_next_step_handler(call.message, callback=edit_remind)


def edit_remind(message: Message):
    if message.text == "/delete":
        bot_client.send_message(chat_id=message.chat.id,
                                text="Are you sure?",
                                reply_markup=get_y_o_r_markup())
        return
    elif message.text == "/cansel":
        bot_client.send_message(chat_id=message.chat.id,
                                text=f"<b>Cansel editing.</b>\n\n"
                                     "Send /show to view all your reminders.\n"
                                     "Send /create to create new remind.",
                                parse_mode="HTML")
        return
    usr = Profile.objects.get(telegram_id=message.chat.id)
    cur_rem = CurrentRemind.objects.get(telegram_id=usr)
    rem = Remind.objects.get(id=cur_rem.rem_id)
    title = message.text.split("\n")[0]
    content = message.text.split("\n")[1:]
    content = " ".join(content).strip()

    rem.title = title
    rem.content = content
    rem.save()

    bot_client.send_message(chat_id=message.chat.id, text=f"<b>Remind edited.</b>\n\n"
                                                          f"Send /show to view all your reminders.\n"
                                                          f"Send /create to create new remind.",
                            parse_mode="HTML")
