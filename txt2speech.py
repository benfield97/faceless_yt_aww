import os
import json
from elevenlabs import voices, generate
import wave
import re

# Get the Eleven Labs API key
eleven_api = os.getenv('ELEVEN_API_KEY')

# Constants
AUDIO_FORMAT = "audio/wav"
BASE_FOLDER_PATH = "audio"
SAMPLE_RATE = 44100
NUM_CHANNELS = 2
SAMPLE_WIDTH = 2
test =0 

# Ensure base folder exists
os.makedirs(BASE_FOLDER_PATH, exist_ok=True)

def sanitize_filename(filename):
    return re.sub(r'[\\/:"*?<>|]', '', filename)

def sanitize_text(text):
    # Remove URLs
    text = re.sub(r'http\S+|www.\S+', '', text, flags=re.MULTILINE)
    # Remove all non-alphabet, non-numeric, non-whitespace characters
    text = re.sub(r'[^\w\s]', '', text)
    return text

def write_audio_file(file_path, audio_data):
    with wave.open(file_path, 'w') as wav_file:
        wav_file.setnchannels(NUM_CHANNELS)
        wav_file.setsampwidth(SAMPLE_WIDTH)
        wav_file.setframerate(SAMPLE_RATE)
        wav_file.writeframes(audio_data)

# Load posts
with open('posts.json', 'r') as f:
    posts = json.load(f)

# Fetch available voices
available_voices = voices()

# Iterate over posts
for post_id, post_details in posts.items():

    # Clean the text in the title
    clean_title = sanitize_text(post_details['title'])

    # Generate and write audio for the post title
    audio = generate(text=clean_title, voice=available_voices[0])
    audio_file_path = os.path.join(BASE_FOLDER_PATH, post_id + '.wav')
    write_audio_file(audio_file_path, audio)

    # Store the path of the wav file
    post_details['TitleWavPath'] = audio_file_path

# Save the updated posts back to the JSON file
with open('posts.json', 'w') as f:
    json.dump(posts, f, indent=4)


#add some more emotion into voice