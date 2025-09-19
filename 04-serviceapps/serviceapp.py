"""
Webex One 2025 - Exploring the possibilities of Webex APIs

- Adam Weeks
- Diego Manuel Jimenez Moreno
- Phil Bellanti
"""

import requests
import json
import os
import datetime
from dotenv import load_dotenv

# This environment variable is often set for local development to allow insecure HTTP for OAuth.
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

'''
The below values are produced by registering a service app on Webex Developer Portal @ developer.webex.com
The scopes selected for this app to run must be meeting:admin_schedule_write due to the 
impersonation functionality set in the create meeting API call that is happening via the 
hostEmail parameter being set. 
replace the below values once the service app is registered and the app is authorized by an org admin
'''
# Load environment variables from the .env file
load_dotenv()

clientID = os.getenv("CLIENTID") # Client ID for your Webex service app
secretID = os.getenv("SECRETID") # Client Secret for your Webex service app
access_token = os.getenv("WEBEX_ACCESS_TOKEN") # Access token obtained after admin authorization
refresh_token = os.getenv("REFRESH_TOKEN") # Refresh token obtained after admin authorization

"""
Function Name : get_tokens_refresh()
Description : This is a utility function that leverages the refresh token
              in exchange for a fresh access_token and refresh_token
              when a 401 is received when using an invalid access_token
              while making an api_call().
              NOTE: in production, auth tokens would not be stored
              in a Session. This app will request a new token each time
              it runs which will not be able to check against expired tokens. 
"""
def get_tokens_refresh():
    print("function : get_token_refresh()")
    
    url = "https://webexapis.com/v1/access_token"
    headers = {'accept':'application/json','content-type':'application/x-www-form-urlencoded'}
    payload = ("grant_type=refresh_token&client_id={0}&client_secret={1}&"
                    "refresh_token={2}").format(clientID, secretID, refresh_token)
    req = requests.post(url=url, data=payload, headers=headers)
    results = json.loads(req.text)

    print("Token returned in refresh result : ", results["access_token"])
    print("Refresh Token returned in refresh result : ", results["refresh_token"])
    return results["access_token"], results["refresh_token"]

"""
Function Name : create_meeting()
Description : This is a function that uses the access_token 
              to create a meeting on behalf of a subuser in 
              a webex organization.
"""
def create_meeting() :
    # Calculate meeting start and end times (24 and 25 hours from now, respectively)
    my_date_start = (datetime.datetime.now() + datetime.timedelta(hours=24)).replace(microsecond=0).isoformat()
    my_date_end = (datetime.datetime.now() + datetime.timedelta(hours=25)).replace(microsecond=0).isoformat()

    body = {
    'title': 'Example Meeting Title',                  # String, Required | Meeting title. The title can be a maximum of 128 characters long.
    'start': my_date_start,                            # String, Required | https://en.wikipedia.org/wiki/ISO_8601 format
    'end':   my_date_end,                              # String, Required | Replace the start/end with the times you'd like
    'hostEmail' : 'A sub users email'
    }

    headers = {
        'Authorization': f'Bearer {access_token}',         # https://oauth.net/2/bearer-tokens/
        'Content-Type': 'application/json',                # https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Objects/JSON
    }

    response = requests.post('https://webexapis.com/v1/meetings', headers=headers, data=json.dumps(body)) # https://developer.webex.com/docs/meetings

    if response.status_code == 200:
        print('statusCode:', response.status_code)
        print(response.json())
    else:
        print('Error:', response.status_code, response.text)
    return response

#the below line is commented out, but will force the app to produce a 401 and invoke the refresh token function
#access_token += 'joe'

#print("before call", access_token)
response = create_meeting()

if (response.status_code == 401) :
    access_token, refresh_token = get_tokens_refresh()
    create_meeting()
