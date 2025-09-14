from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

from webex_bot.commands.echo import EchoCommand
from webex_bot.webex_bot import WebexBot

bot_token = os.getenv("BOT_TOKEN")
name = os.getenv("NAME")
email = os.getenv("EMAIL")

# Create a Bot Object
bot = WebexBot(teams_bot_token=bot_token,
               bot_name="WebexOne2025",
               include_demo_commands=True)

# Call `run` for the bot to wait for incoming messages.
bot.run()
