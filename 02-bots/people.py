from webexpythonsdk import WebexAPI

BOT_TOKEN = "bot_token"

webex = WebexAPI(bot=BOT_TOKEN)

def all_people():
    try:
        all_people = webex.people.list()
        for person in all_people:
            print(f"Name: {person.displayName}, Email: {person.emails}")
    except Exception as e:
        print(f"An error occurred: {e}")

def find_people(name :str):
    try:
        all_people = webex.people.list()
        for person in all_people:
            print(f"Name: {person.displayName}, Email: {person.emails}")
    except Exception as e:
        print(f"An error occurred: {e}")


find_people(name="Char")
all_people()
