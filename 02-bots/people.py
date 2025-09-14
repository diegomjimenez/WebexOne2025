from webexpythonsdk import WebexAPI
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

bot_token = os.getenv("BOT_TOKEN")
name = "USERNAME"

webex = WebexAPI(bot_token)

def all_people():
    try:
        all_people = webex.people.list()
        for person in all_people:
            print(f"Name: {person.displayName}, Email: {person.emails}")
    except Exception as e:
        print(f"An error occurred: {e}")

def find_people(name :str):
    try:
        all_people = webex.people.list(displayName=name)
        for person in all_people:
            print(f"Name: {person.displayName}, Email: {person.emails}")
    except Exception as e:
        print(f"An error occurred: {e}")


find_people(name=name)

all_people()
