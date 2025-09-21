"""
Webex One 2025 - Exploring the possibilities of Webex APIs

- Adam Weeks
- Diego Manuel Jimenez Moreno
- Phil Bellanti
"""

import os
from dotenv import load_dotenv
from webex_bot.webex_bot import WebexBot # Import the main WebexBot class.
from webex_bot.models.command import Command # Import the Command base class for creating custom commands.
from webexpythonsdk import WebexAPI # Import the Webex API SDK for direct API calls.

# Load environment variables from the .env file.
load_dotenv()

# Webex Bot Token for authentication.
bot_token = os.getenv("BOT_TOKEN")
# Approved domain for bot interactions.
domain = os.getenv("DOMAIN")
# Email address (potentially for specific use cases within commands).
email = os.getenv("EMAIL")

# Create a Webex Bot object.
bot = WebexBot(teams_bot_token=bot_token,         # Authenticate the bot with the provided token.
               bot_name="WebexOne2025",            # Assign a name to the bot.
               approved_domains=domain,            # Restrict bot interaction to users from this domain.
               include_demo_commands=False)        # Exclude default demonstration commands.

class SendMessage(Command):
    """
    A custom bot command that, when invoked, sends a direct "Hello!" message
    back to the user who triggered the command.
    """
    def __init__(self):
        # Initialize the command with its keyword and help message.
        super().__init__(
            command_keyword="message",
            help_message="Send Message")

    def execute(self, message, attachment_actions, activity):
        """
        Executes the 'message' command. Sends a "Hello!" message back to the user.

        Args:
            message (str): The message content (command keyword already stripped).
            attachment_actions (obj): Object containing details about card actions (not used directly here).
            activity (obj): Raw activity object from Webex.

        Returns:
            str: A confirmation message to be sent back to the user.
        """
        # Extract the personId of the user who triggered the command from the activity object.
        # This ID identifies the sender of the message to the bot.
        personid = activity.actor.id # Corrected to use activity.actor.id for the sender

        # Initialize a WebexAPI client with the bot token to send a message.
        # This allows the bot to make API calls, such as sending messages.
        webexbot = WebexAPI(bot_token)
        # Create a direct message to the person using their ID with a "Hello!" markdown content.
        webexbot.messages.create(toPersonId=personid, markdown="Hello!")

        # Return a confirmation message to the user that the message was sent.
        return "Message sent"

# Add the custom SendMessage command to the bot.
# This registers the command so the bot can respond to it.
bot.add_command(SendMessage())

# Start the bot and make it listen for incoming messages.
# This call is typically blocking and keeps the bot running, waiting for commands.
bot.run()
