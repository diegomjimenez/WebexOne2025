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
from webex_bot.models.response import Response
from webex_bot.formatting import quote_info
from webexpythonsdk import WebexAPI # Import the Webex API SDK for direct API calls.

# Load environment variables from the .env file.
load_dotenv()

bot_token = os.getenv("BOT_TOKEN")
domain = os.getenv("DOMAIN")
access_token = os.getenv("WEBEX_ACCESS_TOKEN")

# Create a Webex Bot object.
bot = WebexBot(teams_bot_token=bot_token,         # Authenticate the bot with the provided token.
               bot_name="WebexOne2025",            # Assign a name to the bot.
               approved_domains=domain,            # Restrict bot interaction to users from this domain.
               include_demo_commands=False)        # Exclude default demonstration commands.
    
class SendMessageOrganization(Command):

    def __init__(self):
        super().__init__(
            card_callback_keyword="organization_callback",
            delete_previous_message=True)        

    def execute(self, message, attachment_actions, activity):
        message = attachment_actions.inputs.get("message")

        webex = WebexAPI(access_token=access_token)
        webexbot = WebexAPI(bot_token)

        try:
            all_people = webex.people.list()
            for person in all_people:
                webexbot.messages.create(toPersonEmail=person.emails[0], markdown=message)

            return quote_info("Messages sent")
        except Exception as e:
            return quote_info(f"There was an exception when trying to send the messages:\n {e}")

class SendMessageUser(Command):

    def __init__(self):
        super().__init__(
            card_callback_keyword="user_callback",
            delete_previous_message=True)

    def execute(self, message, attachment_actions, activity):
        message = attachment_actions.inputs.get("message")
        user = attachment_actions.inputs.get("user")
        email = user + "@" + domain

        try: 
            # Initialize a WebexAPI client with the bot token to send a message.
            webexbot = WebexAPI(bot_token)
            # Create a direct message to the person using their ID.
            webexbot.messages.create(toPersonEmail=email, markdown=message)

            return quote_info(f"Message sent to user {email}")
        except Exception as e:
            return quote_info(f"There was an exception when trying to send the messages:\n {e}")

class UserMessage(Command):
    """
    A custom bot command to send a direct message to the user who triggered the command.
    """
    def __init__(self):
        # Initialize the command with its keyword and help message.
        super().__init__(
            command_keyword="message_user",
            help_message="Send Message to User",
            delete_previous_message=True,
            chained_commands=[SendMessageUser()])

    def execute(self, message, attachment_actions, activity):
        """
        Executes the 'message' command. Sends a "Hello!" message back to the user.

        Args:
            message (str): The message content (command keyword already stripped).
            attachment_actions (obj): Object containing details about card actions.
            activity (obj): Raw activity object from Webex.

        Returns:
            str: A confirmation message to be sent back to the user.
        """

        card = {
            "contentType": "application/vnd.microsoft.card.adaptive",
            "content": {
                "type": "AdaptiveCard",
                "body": [
                    {
                        "type": "Input.Text",
                        "placeholder": "UserId",
                        "id": "user",
                        "isRequired": True,
                        "errorMessage": "UserId is required",
                        "label": "UserId:"
                    },
                    {
                        "type": "Input.Text",
                        "placeholder": "Message",
                        "id": "message",
                        "isRequired": True,
                        "errorMessage": "Message is required",
                        "label": "Message:"
                    }
                ],
                "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                "version": "1.3",
                "actions": [
                    {
                        "type": "Action.Submit",
                        "title": "Submit",
                        "data": {
                            "callback_keyword": "user_callback"
                        }
                    }
                ]
            }
        }

        response = Response()
        response.text = "Text"
        response.attachments = card

        return response

class OrganizationMessage(Command):
    """
    A custom bot command to send a direct message to the user who triggered the command.
    """
    def __init__(self):
        # Initialize the command with its keyword and help message.
        super().__init__(
            command_keyword="message_organization",
            help_message="Send Message to Organization",
            chained_commands=[SendMessageOrganization()],
            delete_previous_message=True)

    def execute(self, message, attachment_actions, activity):
        """
        Executes the 'message' command. Sends a "Hello!" message back to the user.

        Args:
            message (str): The message content (command keyword already stripped).
            attachment_actions (obj): Object containing details about card actions.
            activity (obj): Raw activity object from Webex.

        Returns:
            str: A confirmation message to be sent back to the user.
        """

        card = {
            "contentType": "application/vnd.microsoft.card.adaptive",
            "content": {
                "type": "AdaptiveCard",
                "body": [
                    {
                        "type": "Input.Text",
                        "placeholder": "Message",
                        "id": "message",
                        "isRequired": True,
                        "errorMessage": "Message is required",
                        "label": "Message:"
                    }
                ],
                "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                "version": "1.3",
                "actions": [
                    {
                        "type": "Action.Submit",
                        "title": "Submit",
                        "data": {
                            "callback_keyword": "organization_callback"
                        }
                    }
                ]
            }
        }

        response = Response()
        response.text = "Text"
        response.attachments = card

        return response

# Add the custom SendMessage command to the bot.
bot.add_command(OrganizationMessage())
bot.add_command(UserMessage())

# This call is typically blocking and keeps the bot running.
bot.run()
