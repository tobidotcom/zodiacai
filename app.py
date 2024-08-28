from flask import Flask, request, jsonify
import openai
import os
import requests
from dotenv import load_dotenv

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Check if the API key is loaded
if not OPENAI_API_KEY:
    raise ValueError("API key is missing in the .env file.")

openai.api_key = OPENAI_API_KEY

@app.route('/moon-reading', methods=['POST'])
def moon_reading():
    try:
        # Get JSON data from the request
        data = request.get_json()
        name = data.get('name')
        zodiac_sign = data.get('zodiac_sign')
        birth_date = data.get('birth_date')
        birth_location = data.get('birth_location')
        birth_time = data.get('birth_time')

        # Validate input data
        if not all([name, zodiac_sign, birth_date, birth_location, birth_time]):
            return jsonify({'error': 'Missing required fields'}), 400

        # Generate the moon reading prompt
        prompt = (f"Generate a personalized moon reading for a person named {name} with zodiac sign {zodiac_sign}, "
                  f"born on {birth_date} in {birth_location} at {birth_time}.")

        # Call OpenAI API for text generation
        response = openai.Completion.create(
            model="gpt-4",  # Ensure this is the correct model identifier
            prompt=prompt,
            max_tokens=150
        )

        moon_reading_text = response.choices[0].text.strip()

        # Call OpenAI TTS API for speech generation
        tts_response = requests.post(
            'https://api.openai.com/v1/audio/speech',
            headers={
                'Authorization': f'Bearer {OPENAI_API_KEY}',
                'Content-Type': 'application/json'
            },
            json={
                'model': 'tts-1',  # Make sure this model is correct
                'input': moon_reading_text,
                'voice': 'onyx',  # Replace with the desired voice
                'response_format': 'mp3'
            }
        )

        if tts_response.status_code == 200:
            return tts_response.content, 200, {'Content-Type': 'audio/mp3'}
        else:
            return jsonify({'error': 'Failed to generate audio from text'}), tts_response.status_code

    except Exception as e:
        # Log the error and return a 500 status code
        print(f"Error: {e}")
        return jsonify({'error': 'Failed to generate moon reading'}), 500

if __name__ == '__main__':
    app.run(debug=True)
