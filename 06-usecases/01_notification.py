"""
Webex One 2025 - Exploring the possibilities of Webex APIs

- Adam Weeks
- Diego Manuel Jimenez Moreno
- Phil Bellanti
"""

import os
from dotenv import load_dotenv
from webex_bot.webex_bot import WebexBot  # Import the main WebexBot class for creating and managing the bot.
from webex_bot.models.command import Command  # Import the Command base class for creating custom bot commands.
from webex_bot.models.response import Response  # Import Response for sending rich replies, like Adaptive Cards.
from webex_bot.formatting import quote_info  # Import quote_info for formatting messages as quoted text.
from webexpythonsdk import WebexAPI  # Import the Webex API SDK for making direct Webex API calls.

# Load environment variables from the .env file.
load_dotenv()

# Webex Bot Token for authentication with the Webex API.
bot_token = os.getenv("BOT_TOKEN")
# Approved domain for bot interactions.
domain = os.getenv("DOMAIN")
# Access token for broader API operations (e.g., listing all people in an org).
access_token = os.getenv("WEBEX_ACCESS_TOKEN")
# The specific email address that is allowed to execute restricted commands.
email = os.getenv("EMAIL")

# Initialize the global WebexAPI client with the bot token.
webex = WebexAPI(bot_token)

# Create a Webex Bot object.
bot = WebexBot(teams_bot_token=bot_token,         # Authenticate the bot using its token.
               bot_name="WebexOne2025",            # Assign a name to the bot.
               approved_domains=domain,            # Set an approved domain to restrict bot usage.
               include_demo_commands=False)        # Exclude default demonstration commands for a cleaner bot.

def is_allowed_sender(person_id: str) -> bool:
    """
    Checks if the user identified by person_id has an email matching ALLOWED_SENDER_EMAIL.

    Args:
        person_id (str): The ID of the person to check.

    Returns:
        bool: True if the user's email matches ALLOWED_SENDER_EMAIL, False otherwise.
    """
    try:
        # Retrieve the person's details using their ID.
        person = webex.people.get(person_id)
        print(f"DEBUG: Checking sender {person.emails[0]} (ID: {person_id}) against allowed email {email}")
        # Compare the user's primary email (or any email) to the allowed email.
        # Case-insensitive comparison is good practice.
        if person.emails and email.lower() in [e.lower() for e in person.emails]:
            return True
        return False
    except Exception as e:
        print(f"DEBUG: Error retrieving person details for {person_id} for access check: {e}")
        return False
    
class SendMessageOrganization(Command):
    """
    Callback command for sending a message to all users in the organization.
    Only the user specified by ALLOWED_SENDER_EMAIL can execute this.
    """
    def __init__(self):
        super().__init__(
            card_callback_keyword="organization_callback", # Keyword for Adaptive Card submission.
            delete_previous_message=True)                 # Deletes the card after submission.

    def execute(self, message, attachment_actions, activity):
        # Extract the message content from the submitted Adaptive Card.
        message_content = attachment_actions.inputs.get("message")
        # Get the personId of the user who submitted the card.
        sender_person_id = attachment_actions.personId

        # --- Access Check ---
        print(f"DEBUG: SendMessageOrganization callback triggered by person ID: {sender_person_id}")
        if not is_allowed_sender(sender_person_id):
            print(f"DEBUG: Unauthorized execution attempt by {sender_person_id}.")
            return quote_info("Error: You are not authorized to send messages to the entire organization.")
        print(f"DEBUG: Authorized sender {sender_person_id} executing SendMessageOrganization.")
        # --- End Access Check ---

        # Initialize WebexAPI clients. One with the access_token for listing people,
        # and another with the bot_token for sending messages.
        # Note: webex_admin requires a full access_token, not a bot_token, to list all org people.
        webex_for_org_list = WebexAPI(access_token=access_token)
        webexbot_for_sending = WebexAPI(bot_token)

        try:
            # List all people in the organization using the admin access_token.
            # Convert GeneratorContainer to list to iterate.
            all_people = list(webex_for_org_list.people.list())
            print(f"DEBUG: Found {len(all_people)} people in the organization.")
            for person in all_people:
                # Send the message to each person.
                webexbot_for_sending.messages.create(toPersonEmail=person.emails[0], markdown=message_content)
                print(f"DEBUG: Message sent to {person.emails[0]}")

            return quote_info("Messages sent to all users in the organization.")
        except Exception as e:
            print(f"DEBUG: Exception in SendMessageOrganization: {e}")
            return quote_info(f"There was an exception when trying to send the messages:\n {e}")

class SendMessageUser(Command):
    """
    Callback command for sending a message to a specific user.
    Only the user specified by ALLOWED_SENDER_EMAIL can execute this.
    """
    def __init__(self):
        super().__init__(
            card_callback_keyword="user_callback", # Keyword for Adaptive Card submission.
            delete_previous_message=True)          # Deletes the card after submission.

    def execute(self, message, attachment_actions, activity):
        # Extract the message content and target username from the submitted Adaptive Card.
        message_content = attachment_actions.inputs.get("message")
        user_id_part = attachment_actions.inputs.get("user")
        target_email = user_id_part + "@" + domain
        # Get the personId of the user who submitted the card.
        sender_person_id = attachment_actions.personId

        # --- Access Check ---
        print(f"DEBUG: SendMessageUser callback triggered by person ID: {sender_person_id}")
        if not is_allowed_sender(sender_person_id):
            print(f"DEBUG: Unauthorized execution attempt by {sender_person_id}.")
            return quote_info("Error: You are not authorized to send messages to specific users.")
        print(f"DEBUG: Authorized sender {sender_person_id} executing SendMessageUser.")
        # --- End Access Check ---

        try: 
            # Initialize a WebexAPI client with the bot token to send a message.
            webexbot_for_sending = WebexAPI(bot_token)
            # Create a direct message to the specified user's email.
            webexbot_for_sending.messages.create(toPersonEmail=target_email, markdown=message_content)
            print(f"DEBUG: Message sent to {target_email}")

            return quote_info(f"Message sent to user {target_email}")
        except Exception as e:
            print(f"DEBUG: Exception in SendMessageUser: {e}")
            return quote_info(f"There was an exception when trying to send the messages:\n {e}")

class UserMessage(Command):
    """
    Command to present an Adaptive Card for sending a message to a specific user.
    Only the user specified by ALLOWED_SENDER_EMAIL can execute this.
    """
    def __init__(self):
        super().__init__(
            command_keyword="message_user",        # Keyword for user to type.
            help_message="Send Message to User",   # Help message for the command.
            delete_previous_message=True,          # Deletes the command message after card is sent.
            chained_commands=[SendMessageUser()])  # Links to SendMessageUser for card submission.

    def execute(self, message, attachment_actions, activity):
        # Get the personId of the user who typed the command.
        sender_person_id = attachment_actions.personId

        # --- Access Check ---
        print(f"DEBUG: UserMessage command triggered by person ID: {sender_person_id}")
        if not is_allowed_sender(sender_person_id):
            print(f"DEBUG: Unauthorized execution attempt by {sender_person_id}.")
            return quote_info("Error: You are not authorized to use this command.")
        print(f"DEBUG: Authorized sender {sender_person_id} executing UserMessage.")
        # --- End Access Check ---

        # Define the Adaptive Card structure for user input.
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
                        "label": "User ID (before @domain):"
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
                             "callback_keyword": "user_callback" # Links to SendMessageUser.
                        }
                    }
                ]
            }
        }

        # Create a Response object to send the Adaptive Card.
        response = Response()
        response.text = "Please provide user details and message:" # Fallback text.
        response.attachments = card

        return response

class OrganizationMessage(Command):
    """
    Command to present an Adaptive Card for sending a message to the entire organization.
    Only the user specified by ALLOWED_SENDER_EMAIL can execute this.
    """
    def __init__(self):
        super().__init__(
            command_keyword="message_organization",        # Keyword for user to type.
            help_message="Send Message to Organization",   # Help message for the command.
            chained_commands=[SendMessageOrganization()],  # Links to SendMessageOrganization for card submission.
            delete_previous_message=True)                  # Deletes the command message after card is sent.

    def execute(self, message, attachment_actions, activity):
        # Get the personId of the user who typed the command.
        sender_person_id = attachment_actions.personId

        # --- Access Check ---
        print(f"DEBUG: OrganizationMessage command triggered by person ID: {sender_person_id}")
        if not is_allowed_sender(sender_person_id):
            print(f"DEBUG: Unauthorized execution attempt by {sender_person_id}.")
            return quote_info("Error: You are not authorized to use this command.")
        print(f"DEBUG: Authorized sender {sender_person_id} executing OrganizationMessage.")
        # --- End Access Check ---

        # Define the Adaptive Card structure for user input.
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
                        "label": "Message to send to all:"
                    }
                ],
                "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                "version": "1.3",
                "actions": [
                    {
                        "type": "Action.Submit",
                        "title": "Submit",
                        "data": {
                            "callback_keyword": "organization_callback" # Links to SendMessageOrganization.
                        }
                    }
                ]
            }
        }

        # Create a Response object to send the Adaptive Card.
        response = Response()
        response.text = "Please enter the message for the organization:" # Fallback text.
        response.attachments = card

        return response

# Add the custom commands to the bot.
bot.add_command(OrganizationMessage())
bot.add_command(UserMessage())

# Start the bot and make it listen for incoming messages.
bot.run()
