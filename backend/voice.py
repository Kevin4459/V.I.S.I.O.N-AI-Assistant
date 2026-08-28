import sounddevice as sd
import numpy as np
import whisper


class VoiceInput:

    def __init__(self, sample_rate=16000, duration=5):
        self.sample_rate = sample_rate
        self.duration = duration

        print("Loading Whisper...")
        self.model = whisper.load_model("tiny")
        print("Whisper loaded.")

    def listen(self):

        print(f"Listening for {self.duration} seconds...")

        audio = sd.rec(
            int(self.duration * self.sample_rate),
            samplerate=self.sample_rate,
            channels=1,
            dtype="float32"
        )

        sd.wait()

        print("Finished listening.")
        print("Transcribing...")

        result = self.model.transcribe(
            audio.flatten(),
            fp16=False
        )

        text = result["text"].strip()

        if text:
            print(f"VISION HEARD: {text}")
            return text

        return None


if __name__ == "__main__":

    voice = VoiceInput()

    while True:

        try:

            text = voice.listen()

            if text:
                print(f"\nYou: {text}\n")
            else:
                print("I didn't hear anything.")

        except KeyboardInterrupt:

            print("\nVoice input shutting down.")
            break