from webexpythonsdk import WebexAPI

from webexpythonsdk import WebexAPI
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

bot_token = os.getenv("BOT_TOKEN")
name = os.getenv("NAME")

webex = WebexAPI(bot_token)

def send_teams_message(bot_token, message, person_email):
    webexbot = WebexAPI(bot_token)
    webexbot.messages.create(toPersonEmail=person_email, markdown=message)

def find_people(name :str):
    try:
        all_people = webex.people.list(displayName=name)
        for person in all_people:
            return person
    except Exception as e:
        print(f"An error occurred: {e}")

person = find_people(name=name)

send_teams_message(bot_token, f"Hello {person.displayName}!", person.emails[0])
