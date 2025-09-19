"""
Webex One 2025 - Exploring the possibilities of Webex APIs

- Adam Weeks
- Diego Manuel Jimenez Moreno
- Phil Bellanti
"""

import os
from dotenv import load_dotenv
# Import specific command (EchoCommand) if needed for custom bot functionality.
from webex_bot.commands.echo import EchoCommand
# Import the main WebexBot class from the webex_bot library.
from webex_bot.webex_bot import WebexBot

# Load environment variables from the .env file.
load_dotenv()

# Webex Bot Token for authentication with the Webex API.
bot_token = os.getenv("BOT_TOKEN")

# Create a Webex Bot object.
bot = WebexBot(teams_bot_token=bot_token,         # Authenticate the bot with the provided token.
               bot_name="WebexOne2025",            # Assign a name to the bot.
               include_demo_commands=True)         # Include default demonstration commands (e.g., 'echo', 'help').

# Start the bot and make it listen for incoming messages.
bot.run()
