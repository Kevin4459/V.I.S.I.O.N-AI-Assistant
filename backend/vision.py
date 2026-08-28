import requests

from config import (
    VISION_NAME,
    VISION_VERSION,
    OLLAMA_URL,
    MODEL
)

from personality import SYSTEM_PROMPT
from memory import ConversationMemory
from voice import VoiceInput


class Vision:

    def __init__(self):

        self.memory = ConversationMemory()

        self.system_message = {
            "role": "system",
            "content": SYSTEM_PROMPT
        }

    def think(self, user_input):

        self.memory.add_user_message(user_input)

        messages = [
            self.system_message,
            *self.memory.get_messages()
        ]

        payload = {
            "model": MODEL,
            "messages": messages,
            "stream": False
        }

        try:

            response = requests.post(
                OLLAMA_URL,
                json=payload,
                timeout=120
            )

            response.raise_for_status()

            data = response.json()

            answer = data["message"]["content"]

            self.memory.add_assistant_message(answer)

            return answer

        except requests.exceptions.ConnectionError:

            return (
                "I cannot connect to Ollama. "
                "Please make sure Ollama is running."
            )

        except requests.exceptions.Timeout:

            return "The model took too long to respond."

        except Exception as error:

            return f"An error occurred: {error}"


def main():

    vision = Vision()
    voice = VoiceInput()

    print()
    print("=" * 60)

    print(f"{VISION_NAME} V{VISION_VERSION}")

    print(
        "Virtual Intelligence System for "
        "Integrated Operations and Navigation"
    )

    print("=" * 60)
    print()

    print("VISION is online.")
    print()

    print("Select input mode:")
    print("[1] Text")
    print("[2] Voice")
    print("[3] Exit")
    print()

    while True:

        try:

            mode = input("Mode: ").strip()

            if mode == "3":

                print()
                print("VISION: Shutting down.")
                break

            if mode not in ["1", "2"]:

                print("Please select 1, 2, or 3.")
                continue

            # -----------------------------
            # TEXT INPUT
            # -----------------------------

            if mode == "1":

                user_input = input("You: ").strip()

            # -----------------------------
            # VOICE INPUT
            # -----------------------------

            else:

                user_input = voice.listen()

                if not user_input:

                    print()
                    print("VISION: I didn't hear anything.")
                    print()

                    continue

                print()
                print(f"You: {user_input}")

            # -----------------------------
            # EXIT COMMANDS
            # -----------------------------

            if user_input.lower() in [
                "exit",
                "quit",
                "shutdown"
            ]:

                print()
                print("VISION: Shutting down.")
                break

            # -----------------------------
            # VISION THINKS
            # -----------------------------

            response = vision.think(user_input)

            print()
            print(f"VISION: {response}")
            print()

        except KeyboardInterrupt:

            print()
            print("VISION: Shutting down.")
            break


if __name__ == "__main__":
    main()