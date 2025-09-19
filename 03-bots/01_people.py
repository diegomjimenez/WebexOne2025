"""
Webex One 2025 - Exploring the possibilities of Webex APIs

- Adam Weeks
- Diego Manuel Jimenez Moreno
- Phil Bellanti
"""

import os
from dotenv import load_dotenv
from webexpythonsdk import WebexAPI

# Load environment variables from the .env file.
load_dotenv()

# Webex Bot Token for API authentication.
bot_token = os.getenv("BOT_TOKEN")
# Email address for user lookup.
email = os.getenv("EMAIL")

# Initialize the WebexAPI client with the bot token.
webex = WebexAPI(bot_token)

def all_people():
    """
    Retrieves and prints the display name and email(s) for all people
    accessible by the authenticated Webex bot/user.
    """
    try:
        # List all people in the organization.
        all_people = webex.people.list()
        # Iterate through the list of people and print their details.
        for person in all_people:
            print(f"Name: {person.displayName}, Email: {person.emails}")
    except Exception as e:
        # Catch and print any exceptions that occur during the API call.
        print(f"An error occurred while listing all people: {e}")

def find_people(email_address: str):
    """
    Finds and prints the display name and email(s) for a specific person
    based on their email address.

    Args:
        email_address (str): The email address of the person to find.
    """
    try:
        # List people, filtering by the provided email address.
        found_people = webex.people.list(email=email_address)
        # Iterate through the (potentially single) person found and print their details.
        for person in found_people:
            print(f"Name: {person.displayName}, Email: {person.emails}")
    except Exception as e:
        # Catch and print any exceptions that occur during the API call.
        print(f"An error occurred while finding people by email: {e}")

# Call the find_people function using the email loaded from environment variables.
find_people(email_address=email)

# Call the all_people function to list all accessible users.
all_people()
