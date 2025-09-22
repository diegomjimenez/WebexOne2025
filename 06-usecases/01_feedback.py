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
# The specific email address that is allowed to execute restricted commands AND will receive feedback.
email = os.getenv("EMAIL")

# Initialize the global WebexAPI client with the bot token.
# This client can be used for general API calls, like getting user details.
webex = WebexAPI(bot_token)

# Create a Webex Bot object.
bot = WebexBot(teams_bot_token=bot_token,         # Authenticate the bot using its token.
               bot_name="WebexOne2025",            # Assign a name to the bot.
               approved_domains=domain,            # Set an approved domain to restrict bot usage.
               include_demo_commands=False)        # Exclude default demonstration commands for a cleaner bot.

def get_sender_email_from_person_id(person_id: str) -> str:
    """
    Retrieves the primary email address of a user given their person ID.

    Args:
        person_id (str): The ID of the person.

    Returns:
        str: The primary email address of the person, or "unknown@example.com" if not found/error.
    """
    try:
        person = webex.people.get(person_id)
        if person.emails:
            return person.emails[0]
        return "unknown@example.com"
    except Exception as e:
        print(f"DEBUG: Error retrieving email for person ID {person_id}: {e}")
        return "unknown@example.com"

def is_allowed_sender(person_id: str) -> bool:
    """
    Checks if the user identified by person_id has an email matching Admin Email.

    Args:
        person_id (str): The ID of the person to check.

    Returns:
        bool: True if the user's email matches Admin Email, False otherwise.
    """
    if not email:
        print("DEBUG: Admin Email is not set in .env. All users are implicitly blocked from restricted commands.")
        return False # If no allowed email is configured, no one is allowed.

    try:
        # Retrieve the person's details using their ID.
        person = webex.people.get(person_id)
        current_user_email = person.emails[0].lower() if person.emails else ""
        print(f"DEBUG: Checking sender {current_user_email} (ID: {person_id}) against allowed email {email.lower()}")
        # Compare the user's primary email to the allowed email. Case-insensitive comparison.
        if current_user_email == email.lower():
            return True
        return False
    except Exception as e:
        print(f"DEBUG: Error retrieving person details for {person_id} for access check: {e}")
        return False

class SubmitFeedbackCommand(Command):
    """
    This class handles the submission of the feedback Adaptive Card.
    It's a chained command, triggered by the card's submit action.
    """
    def __init__(self):
        super().__init__(
            card_callback_keyword="feedback_submit", # Keyword used by the Adaptive Card's submit action.
            delete_previous_message=True)            # Deletes the Adaptive Card after submission.

    def execute(self, message, attachment_actions, activity):
        # Extract the feedback text from the submitted Adaptive Card's inputs.
        feedback_text = attachment_actions.inputs.get("feedback_input")
        # Get the personId of the user who submitted the card.
        sender_person_id = attachment_actions.personId
        sender_email = get_sender_email_from_person_id(sender_person_id)

        print(f"DEBUG: Feedback submitted by {sender_email} (ID: {sender_person_id})")
        print(f"DEBUG: Feedback content: '{feedback_text}'")

        # Initialize a WebexAPI client to send the feedback to the designated email.
        webexbot_for_sending = WebexAPI(bot_token)
        
        try:
            # Construct the message to be sent to the feedback recipient (your email).
            feedback_message_to_you = f"**New Feedback Received!**\n\n" \
                                      f"**From:** {sender_email}\n" \
                                      f"**Feedback:**\n```\n{feedback_text}\n```"
            
            # Send the feedback to the Admin Email.
            webexbot_for_sending.messages.create(toPersonEmail=email, markdown=feedback_message_to_you)
            print(f"DEBUG: Feedback successfully forwarded to {email}")

            # Return a confirmation message to the user who submitted the feedback.
            return quote_info("Thank you for your feedback! It has been submitted.")
        except Exception as e:
            print(f"DEBUG: Error sending feedback to {email}: {e}")
            return quote_info(f"There was an error submitting your feedback. Please try again later. Error: {e}")

class SendFeedbackToAllCommand(Command):
    """
    This command, when triggered by an authorized user, sends an Adaptive Card
    to ALL users in the organization to collect feedback.
    """
    def __init__(self):
        super().__init__(
            command_keyword="feedback", # The keyword users type to activate this command.
            help_message="Send feedback card to all users in the organization",
            chained_commands=[SubmitFeedbackCommand()], # Links to SubmitFeedbackCommand for card submission.
            delete_previous_message=True) 

    def execute(self, message, attachment_actions, activity):
        # Get the personId of the user who typed the command.
        sender_person_id = attachment_actions.personId
        sender_email = get_sender_email_from_person_id(sender_person_id)

        print(f"DEBUG: SendFeedbackToAllCommand triggered by {sender_email} (ID: {sender_person_id})")

        # --- Access Check ---
        if not is_allowed_sender(sender_person_id):
            print(f"DEBUG: Unauthorized user {sender_email} attempted to execute SendFeedbackToAllCommand.")
            return quote_info("Error: You are not authorized to send feedback requests to the entire organization.")
        print(f"DEBUG: Authorized sender {sender_email} executing SendFeedbackToAllCommand.")
        # --- End Access Check ---

        # Initialize a WebexAPI client using the admin-level access_token
        # to list all people in the organization.
        webex_admin_client = WebexAPI(access_token=access_token)
        
        # Define the Adaptive Card structure for feedback input.
        feedback_card_content = {
            "type": "AdaptiveCard",
            "body": [
                {
                    "type": "TextBlock",
                    "text": "We'd love to hear your thoughts!",
                    "wrap": True,
                    "size": "Medium",
                    "weight": "Bolder"
                },
                {
                    "type": "Input.Text",
                    "placeholder": "Enter your feedback here...",
                    "id": "feedback_input", # This ID will be used to extract the input value.
                    "isMultiline": True,
                    "isRequired": True,
                    "errorMessage": "Feedback cannot be empty.",
                    "label": "Your Feedback:"
                }
            ],
            "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
            "version": "1.3",
            "actions": [
                {
                    "type": "Action.Submit",
                    "title": "Submit Feedback",
                    "data": {
                        "callback_keyword": "feedback_submit" # This links to SubmitFeedbackCommand.
                    }
                }
            ]
        }
        feedback_card = {
            "contentType": "application/vnd.microsoft.card.adaptive",
            "content": feedback_card_content
        }

        try:
            # List all people in the organization.
            all_people = list(webex_admin_client.people.list())
            print(f"DEBUG: Found {len(all_people)} people in the organization to send feedback card to.")

            # Send the Adaptive Card to each person.
            for person in all_people:
                if person.emails: # Ensure the person has an email address.
                    try:
                        webex.messages.create(
                            toPersonEmail=person.emails[0],
                            text="Please provide your feedback:", # Fallback text.
                            attachments=[feedback_card]
                        )
                        print(f"DEBUG: Feedback card sent to {person.emails[0]}")
                    except Exception as send_e:
                        print(f"DEBUG: Error sending feedback card to {person.emails[0]}: {send_e}")
            
            return quote_info("Feedback cards have been sent to all users in the organization.")

        except Exception as e:
            print(f"DEBUG: Error when sending feedback cards to all users: {e}")
            return quote_info(f"An error occurred while trying to send feedback cards to all users: {e}")


# Add the custom commands to the bot.
bot.add_command(SendFeedbackToAllCommand())

# Start the bot and make it listen for incoming messages.
bot.run()
