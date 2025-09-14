from webexpythonsdk import WebexAPI
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

bot_token = os.getenv("BOT_TOKEN")
name = os.getenv("NAME")
email = os.getenv("EMAIL")

webex = WebexAPI(bot_token)

card = {    
    "contentType": "application/vnd.microsoft.card.adaptive",
    "content": 
        PASTE YOUR CARD HERE!
}

webex.messages.create(toPersonEmail=email, text="", attachments=[card])

'''
card_example = {    
    "contentType": "application/vnd.microsoft.card.adaptive",
    "content": 
        {
        "type": "AdaptiveCard",
        "body": [
            {
                "type": "ColumnSet",
                "columns": [
                    {
                        "type": "Column",
                        "items": [
                            {
                                "type": "TextBlock",
                                "weight": "Bolder",
                                "text": "WebexOne",
                                "horizontalAlignment": "Left",
                                "wrap": True,
                                "color": "Light",
                                "size": "Large",
                                "spacing": "Small"
                            }
                        ],
                         "width": "stretch"
                    }
                ]
            },
            {
                "type": "TextBlock",
                "text": "This is my first Adaptive Card!",
                "wrap": True
            }
        ],
        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
        "version": "1.3"
    }
}
'''
