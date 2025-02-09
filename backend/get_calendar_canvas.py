import requests
from bs4 import BeautifulSoup


# API URL for fetching calendar events
url = "https://learn.ontariotechu.ca/api/v1/calendar_events"

# Replace with your actual API token
headers = {
    "Authorization": "Bearer 13377~KYP23997LzK7Mhc6NKNMZkEZMktzQwJK9BTQGTD47RMQTJyHAKxewLrvCnNLXAUX"
}

# Make the request
response = requests.get(url, headers=headers)

# Print response
if response.status_code == 200:
    events = response.json()
    for event in events:
        print(f"Event ID: {event['id']} - Title: {event['title']}")
else:
    print(f"Error: {response.status_code}, {response.text}")

# Canvas API URL - replace {event_id} with an actual event ID
event_id = "12345"  # Replace with a valid event ID
url = f"https://learn.ontariotechu.ca/api/v1/calendar_events/{event_id}"

# API token (replace with your actual token)
headers = {
    "Authorization": "Bearer 13377~KYP23997LzK7Mhc6NKNMZkEZMktzQwJK9BTQGTD47RMQTJyHAKxewLrvCnNLXAUX",
    "Content-Type": "application/json"
}

# Data to update the event
data = {
    "calendar_event": {
        "visible": False,  # Hide the event
        "auto_subscribe": False  # Disable auto-subscription
    }
}

# Make the PUT request to update the event
response = requests.put(url, headers=headers, json=data)

# Print response
print(f"Status Code: {response.status_code}")
print(f"Response Text: {response.text}")

# Error handling
if response.status_code == 401:
    print("⚠️ Unauthorized! Check your API token permissions.")
elif response.status_code == 404:
    print("⚠️ Not Found! Ensure the event ID and API endpoint are correct.")
elif response.status_code != 200:
    print(f"⚠️ Unexpected error: {response.status_code}")

