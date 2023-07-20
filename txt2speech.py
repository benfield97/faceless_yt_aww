import os
import json
import re
from elevenlabs import voices, generate, VoiceSettings
import wave

# Get the Eleven Labs API key
eleven_api = os.getenv('ELEVEN_API_KEY')

# Constants
AUDIO_FORMAT = "audio/wav"
BASE_FOLDER_PATH = "audio"
SAMPLE_RATE = 44100
NUM_CHANNELS = 2
SAMPLE_WIDTH = 2

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

def video_file_exists(post_link_key):
    for filename in os.listdir('vids'):
        if post_link_key in filename:
            return True
    return False

# Load posts
with open('posts.json', 'r') as f:
    posts = json.load(f)

# Fetch the voices
voice_obj = voices()
voice_list = voice_obj.voices

# Create new settings
new_settings = VoiceSettings(stability=0.25, similarity_boost=0.9)

# Modify the settings of the first voice
voice_list[2].settings = new_settings

# Generate speech using the modified voice
voice_choice = voice_list[2]

# Iterate over posts
for post_id, post_details in posts.items():

    # Skip this post if a video file with the post link key in its name DOES NOT exist
    if not video_file_exists(post_details['link']):
        continue

    # Clean the text in the title
    clean_title = sanitize_text(post_details['title'])

    # Generate and write audio for the post title
    audio = generate(text=clean_title, voice=voice_choice,)
    audio_file_path = os.path.join(BASE_FOLDER_PATH, post_id + '.wav')
    write_audio_file(audio_file_path, audio)

    # Store the path of the wav file
    post_details['TitleWavPath'] = audio_file_path

# Save the updated posts back to the JSON file
with open('posts.json', 'w') as f:
    json.dump(posts, f, indent=4)
