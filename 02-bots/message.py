from webexpythonsdk import WebexAPI
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

bot_token = os.getenv("BOT_TOKEN")
email = os.getenv("EMAIL")

webex = WebexAPI(bot_token)

def send_teams_message(bot_token, message, person_email):
    webexbot = WebexAPI(bot_token)
    webexbot.messages.create(toPersonEmail=person_email, markdown=message)

def find_people(email :str):
    try:
        people = webex.people.list(email=email)
        for person in people:
            return person
    except Exception as e:
        print(f"An error occurred: {e}")

person = find_people(email=email)

send_teams_message(bot_token, f"Hello {person.displayName}!", person.emails[0])
