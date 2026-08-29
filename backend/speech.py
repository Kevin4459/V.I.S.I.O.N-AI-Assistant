import os
import tempfile
import subprocess

from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs


load_dotenv()

API_KEY = os.getenv("ELEVENLABS_API_KEY")

if not API_KEY:
    raise ValueError(
        "ELEVENLABS_API_KEY was not found in the .env file."
    )


client = ElevenLabs(
    api_key=API_KEY
)


# Daniel - Steady Broadcaster
VOICE_ID = "onwK4e9ZLuTAKqWW03F9"


def speak(text):

    print("VISION is speaking...")

    audio = client.text_to_speech.convert(
        voice_id=VOICE_ID,
        model_id="eleven_multilingual_v2",
        text=text
    )

    # Convert ElevenLabs audio stream into bytes
    audio_bytes = b"".join(audio)

    # Create a temporary MP3 file
    with tempfile.NamedTemporaryFile(
        suffix=".mp3",
        delete=False
    ) as temp_file:

        temp_file.write(audio_bytes)
        temp_path = temp_file.name

    try:

        # Play the audio using macOS
        subprocess.run(
            ["afplay", temp_path],
            check=True
        )

    finally:

        # Delete temporary audio file
        if os.path.exists(temp_path):
            os.remove(temp_path)


if __name__ == "__main__":

    print("Testing VISION's voice...")

    message = (
        "Hello Kevin. I am VISION. "
        "My voice system is online."
    )

    print(f"VISION: {message}")

    speak(message)