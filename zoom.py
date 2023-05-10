import jwt
import time
import requests
import json
from collections import defaultdict

ZOOM_API_KEY = ''
ZOOM_API_SECRET = ''
ZOOM_MEETING_ID = ''
ZOOM_MEETING_PASSWORD = ''

# Create a JWT token to authenticate with the Zoom API
def generate_jwt(api_key, api_secret):
   header = {"alg": "HS256", "typ": "JWT"}
   token_payload = {"iss": ZOOM_API_KEY, "exp": int(time.time() + 3600)}
   token = jwt.encode(token_payload, ZOOM_API_SECRET, algorithm="HS256", headers=header)
   return token

# Fetch the list of participants for the specified Zoom meeting ID
def fetch_participants(api_key, api_secret, meeting_id, meeting_password):
    token = generate_jwt(api_key, api_secret)
    url = f"https://api.zoom.us/v2/report/meetings/{meeting_id}/participants"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"password": meeting_password}
    response = requests.get(url, headers=headers, params=params)
    return response.json()

# Extract the list of participant email addresses from the Zoom API response
def get_participant_list(api_key, api_secret, meeting_id, meeting_password):
    response = fetch_participants(api_key, api_secret, meeting_id, meeting_password)
    print(response)
    participants = response['participants']
    participant_list = [participant['email'] for participant in participants]
    return participant_list

# Call the get_participant_list function to get a list of participants for the Zoom meeting
participant_list = get_participant_list(ZOOM_API_KEY, ZOOM_API_SECRET, ZOOM_MEETING_ID, ZOOM_MEETING_PASSWORD)

# Print the list of participants
print(participant_list)

# Read the list of names and surnames from the file
with open('list.txt', 'r') as f:
    lines = f.readlines()
names = [line.strip().split(' ') for line in lines]


# İsimlerin sayısını hesaplayın
name_count = defaultdict(int)
for name in names:
    first_name = name[0]
    name_count[first_name.lower()] += 1

# Zoom'daki katılımcıların sayısını hesaplayın
zoom_participant_count = defaultdict(int)
for participant in participant_list:
    for name, count in name_count.items():
        if name.lower() in participant.lower():
            zoom_participant_count[name.lower()] += 1
            break

# Eksik katılımcıları bulun
missing_participants = []
for name, count in name_count.items():
    if zoom_participant_count[name.lower()] < count:
        missing_count = count - zoom_participant_count[name.lower()]
        for i in range(missing_count):
            missing_participants.append(name)

# Eksik katılımcıları yazdır
print('Eksik katılımcılar:')
for participant in missing_participants:
    print(participant)
