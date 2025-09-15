from dotenv import load_dotenv
import os
from webex_bot.commands.echo import EchoCommand
from webex_bot.webex_bot import WebexBot

# Load environment variables from .env file
load_dotenv()

bot_token = os.getenv("BOT_TOKEN")

# Create a Bot Object
bot = WebexBot(teams_bot_token=bot_token,
               bot_name="WebexOne2025",
               include_demo_commands=False)

# Include function and add it.
## Plus remove unnecessary stuff

# Call `run` for the bot to wait for incoming messages.
bot.run()
