"""
Webex One 2025 - Exploring the possibilities of Webex APIs

- Adam Weeks
- Diego Manuel Jimenez Moreno
- Phil Bellanti
"""

import requests # Import the requests library for making HTTP requests.
import os
from dotenv import load_dotenv # Import load_dotenv to load environment variables from .env file.

# Load environment variables from the .env file.
load_dotenv()

# Access token for broader API operations (e.g., listing all people in an org).
access_token = os.getenv("WEBEX_ACCESS_TOKEN")

def list_people(access_token: str, url: str) -> requests.Response:
    """
    Fetches a list of people from the Webex People API using the provided URL and access token.

    Args:
        access_token (str): The Webex access token for authentication.
        url (str): The API endpoint URL to fetch people from (e.g., "https://webexapis.com/v1/people").

    Returns:
        requests.Response: The HTTP response object if the request is successful (status code 200).

    Raises:
        Exception: If the API request fails (status code other than 200).
    """
    # Define the authorization header with the bearer token.
    headers = {
        'Authorization': f"Bearer {access_token}"
    }

    print(f"DEBUG: Making API request to URL: {url}")
    # Send a GET request to the specified URL with the defined headers.
    response = requests.get(url, headers=headers)

    # Check if the request was successful (HTTP status code 200).
    if response.status_code == 200:
        print(f"DEBUG: API request successful. Status Code: {response.status_code}")
        return response
    else:
        # If the request failed, raise an exception with details.
        print(f"DEBUG: API request failed. Status Code: {response.status_code}, Response: {response.text}")
        raise Exception(f"Failed to obtain people: {response.status_code} - {response.text}")

try:
    # Initial URL for the first page of people. Requesting a maximum of 2 people per page for demonstration.
    current_url = "https://webexapis.com/v1/people?max=2"
    page_number = 1
    
    # Loop to fetch all pages of people until no 'next' link is found.
    while current_url:
        print(f"\nDEBUG: Fetching page {page_number} of people.")
        response = list_people(access_token, current_url)
        
        # Parse the JSON response and extract the 'items' array (the list of people).
        people = response.json()["items"]
        
        if people:
            print(f"Printing people from page {page_number}:")
            # Iterate through the retrieved people and print their display name and email(s).
            for person in people:
                print(f"Name: {person['displayName']}, Email: {person['emails']}")
        else:
            print(f"DEBUG: No people found on page {page_number}.")

        # Check for pagination links. If a 'next' link exists, update the URL to fetch the next page.
        if "next" in response.links:
            current_url = response.links["next"]["url"]
            print(f"DEBUG: Found 'next' pagination link. Next URL: {current_url}")
            page_number += 1
        else:
            # If no 'next' link, we've reached the last page, so exit the loop.
            print("DEBUG: No more 'next' pagination links found. All people listed.")
            current_url = None # Exit condition for the while loop
    else:
        print("DEBUG: No 'next' pagination link found. All people have been listed.")

except Exception as e:
    # Catch any exceptions that occurred during the API calls or processing.
    print(f"\nERROR: An unexpected error occurred during execution: {e}")
