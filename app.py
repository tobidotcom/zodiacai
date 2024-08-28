from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Check if the API key is loaded
if not OPENAI_API_KEY:
    raise ValueError("API key is missing in the .env file.")

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

        # Call OpenAI API for chat completion
        chat_response = requests.post(
            'https://api.openai.com/v1/chat/completions',
            headers={
                'Authorization': f'Bearer {OPENAI_API_KEY}',
                'Content-Type': 'application/json'
            },
            json={
                'model': 'gpt-4',
                'messages': [
                    {"role": "system", "content": "You are a helpful assistant that provides moon readings."},
                    {"role": "user", "content": prompt}
                ],
                'max_tokens': 150
            }
        )

        if chat_response.status_code != 200:
            return jsonify({'error': 'Failed to generate moon reading'}), chat_response.status_code

        moon_reading_text = chat_response.json()['choices'][0]['message']['content'].strip()

        # Call OpenAI TTS API for speech generation
        tts_response = requests.post(
            'https://api.openai.com/v1/audio/speech',
            headers={
                'Authorization': f'Bearer {OPENAI_API_KEY}',
                'Content-Type': 'application/json'
            },
            json={
                'model': 'tts-1',
                'input': moon_reading_text,
                'voice': 'onyx',
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