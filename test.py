import requests
import json

# Define the URL of your Flask application
url = 'http://localhost:5000/moon-reading'

# Define the data to send in the POST request
data = {
    "name": "John Doe",
    "zodiac_sign": "Leo",
    "birth_date": "1990-08-15",
    "birth_location": "New York",
    "birth_time": "15:30"
}

# Convert the data to JSON format
headers = {
    'Content-Type': 'application/json'
}

# Make the POST request
response = requests.post(url, headers=headers, data=json.dumps(data))

# Check if the request was successful
if response.status_code == 200:
    # Save the response content (MP3 file) to disk
    with open('moon_reading.mp3', 'wb') as file:
        file.write(response.content)
    print("Moon reading saved as 'moon_reading.mp3'")
else:
    print(f"Failed to generate moon reading. Status code: {response.status_code}")
    print(f"Response: {response.text}")
