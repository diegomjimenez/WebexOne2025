"""
Webex One 2025 - Exploring the possibilities of Webex APIs

- Adam Weeks
- Diego Manuel Jimenez Moreno
- Phil Bellanti
"""

import requests # Import the requests library for making HTTP requests.

# Define a placeholder for your Webex Access Token.
# In a real application, this would be loaded securely from environment variables or a configuration file.
ACCESS_TOKEN = "access_token"

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

# --- Main execution block ---
try:
    # First call to list people, requesting a maximum of 2 people per page.
    print("\nDEBUG: Initiating first API call to list people.")
    response = list_people(ACCESS_TOKEN, "https://webexapis.com/v1/people?max=2")
    
    # Parse the JSON response and extract the 'items' array (the list of people).
    people = response.json()["items"]
    print("Printing first 2 people:")
    # Iterate through the retrieved people and print their display name and email(s).
    for person in people:
        print(f"Name: {person['displayName']}, Email: {person['emails']}")

    # Check for pagination links. If a 'next' link exists, it indicates more results.
    if "next" in response.links:
        links = response.links["next"]["url"]
        print(f"DEBUG: Found 'next' pagination link: {links}")
        
        # Second call to list people, using the 'next' link for pagination.
        print("\nDEBUG: Initiating second API call to list next set of people.")
        response2 = list_people(ACCESS_TOKEN, links)
        
        # Parse the JSON response for the next set of people.
        people2 = response2.json()["items"]
        print("Printing next 2 people:")
        # Iterate through the next set of people and print their details.
        for person in people2:
            print(f"Name: {person['displayName']}, Email: {person['emails']}")
    else:
        print("DEBUG: No 'next' pagination link found. All people have been listed.")

except Exception as e:
    # Catch any exceptions that occurred during the API calls or processing.
    print(f"\nERROR: An unexpected error occurred during execution: {e}")
