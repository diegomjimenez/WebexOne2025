from dotenv import load_dotenv
import os
from webex_bot.webex_bot import WebexBot
from webex_bot.models.command import Command
from webexpythonsdk import WebexAPI

# Load environment variables from .env file
load_dotenv()

bot_token = os.getenv("BOT_TOKEN")
domain = os.getenv("DOMAIN")
email = os.getenv("EMAIL")

# Create a Bot Object
bot = WebexBot(teams_bot_token=bot_token,
               bot_name="WebexOne2025",
               approved_domains=domain,
               include_demo_commands=False)

class SendMessage(Command):

    def __init__(self):
        super().__init__(
            command_keyword="message",
            help_message="Send Message")

    def execute(self, message, attachment_actions, activity):
        """
        :param message: message with command already stripped
        :param attachment_actions: attachment_actions object
        :param activity: activity object

        :return: a string or Response object (or a list of either). Use Response if you want to return another card.
        """
        personid = attachment_actions.personId

        webexbot = WebexAPI(bot_token)
        webexbot.messages.create(toPersonId=personid, markdown="Hello!")

        return "Message sent"

# Include function and add it.
bot.add_command(SendMessage())

# Call `run` for the bot to wait for incoming messages.
bot.run()
