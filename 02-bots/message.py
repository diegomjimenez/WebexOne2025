from webexpythonsdk import WebexAPI

BOT_TOKEN = "bot_token"
NAME = "your_name"

def send_teams_message(bot_token, message, person_email):
    webexbot = WebexAPI(bot_token)
    webexbot.messages.create(toPersonEmail=person_email, markdown=message)

def find_people(name :str):
    try:
        people = webex.people.list()
        for person in people:
            print(f"Name: {person.displayName}, Email: {person.emails}")
    except Exception as e:
        print(f"An error occurred: {e}")

webex = WebexAPI(access_token=BOT_TOKEN)
myself = find_people(name=NAME)
for person in all_people:
    send_teams_message(BOT_TOKEN, f"Hello {person.displayName}!", person.emails[0])
