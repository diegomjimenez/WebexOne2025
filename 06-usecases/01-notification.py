from dotenv import load_dotenv
import os
from webexpythonsdk import WebexAPI

# Load environment variables from .env file
load_dotenv()

bot_token = os.getenv("BOT_TOKEN")
access_token = os.getenv("WEBEX_ACCESS_TOKEN")

def send_teams_message(bot_token, message, person_email):
    webexbot = WebexAPI(bot_token)
    webexbot.messages.create(toPersonEmail=person_email, markdown=message)

webex = WebexAPI(access_token=access_token)
all_people = webex.people.list()
for person in all_people:
    send_teams_message(bot_token, f"Hello {person.displayName}!", person.emails[0])
