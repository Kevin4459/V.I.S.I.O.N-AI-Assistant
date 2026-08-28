import tkinter as tk
from tkinter import scrolledtext
import threading

from vision import Vision
from voice import VoiceInput


class VisionGUI:

    def __init__(self, root):

        self.root = root
        self.root.title("VISION")
        self.root.geometry("700x700")
        self.root.minsize(600, 600)

        # -----------------------------------------
        # VISION BACKEND
        # -----------------------------------------

        self.vision = Vision()

        self.voice = None

        # -----------------------------------------
        # COLORS
        # -----------------------------------------

        self.background_color = "#101216"
        self.chat_color = "#181B21"
        self.input_color = "#20242C"
        self.text_color = "#FFFFFF"
        self.secondary_text = "#A0A6B1"

        # -----------------------------------------
        # MAIN WINDOW
        # -----------------------------------------

        self.root.configure(
            bg=self.background_color
        )

        # -----------------------------------------
        # HEADER
        # -----------------------------------------

        header = tk.Frame(
            root,
            bg=self.background_color
        )

        header.pack(
            fill="x",
            padx=20,
            pady=(20, 10)
        )

        title = tk.Label(
            header,
            text="VISION",
            font=("Helvetica", 26, "bold"),
            fg=self.text_color,
            bg=self.background_color
        )

        title.pack()

        subtitle = tk.Label(
            header,
            text="Virtual Intelligence System",
            font=("Helvetica", 11),
            fg=self.secondary_text,
            bg=self.background_color
        )

        subtitle.pack(
            pady=(2, 0)
        )

        # -----------------------------------------
        # CHAT WINDOW
        # -----------------------------------------

        self.chat = scrolledtext.ScrolledText(
            root,
            wrap=tk.WORD,
            font=("Helvetica", 13),
            bg=self.chat_color,
            fg=self.text_color,
            insertbackground=self.text_color,
            relief="flat",
            padx=15,
            pady=15
        )

        self.chat.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        self.chat.configure(
            state="disabled"
        )

        # -----------------------------------------
        # INPUT AREA
        # -----------------------------------------

        input_frame = tk.Frame(
            root,
            bg=self.background_color
        )

        input_frame.pack(
            fill="x",
            padx=20,
            pady=(5, 10)
        )

        self.entry = tk.Entry(
            input_frame,
            font=("Helvetica", 13),
            bg=self.input_color,
            fg=self.text_color,
            insertbackground=self.text_color,
            relief="flat"
        )

        self.entry.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=12,
            padx=(0, 10)
        )

        self.entry.bind(
            "<Return>",
            self.send_text
        )

        self.send_button = tk.Button(
            input_frame,
            text="Send",
            font=("Helvetica", 11, "bold"),
            command=self.send_text,
            relief="flat",
            padx=20,
            pady=10
        )

        self.send_button.pack(
            side="right"
        )

        # -----------------------------------------
        # VOICE BUTTON
        # -----------------------------------------

        voice_frame = tk.Frame(
            root,
            bg=self.background_color
        )

        voice_frame.pack(
            pady=(5, 25)
        )

        self.voice_button = tk.Button(
            voice_frame,
            text="🎤  LISTEN",
            font=("Helvetica", 14, "bold"),
            command=self.start_voice,
            relief="flat",
            padx=40,
            pady=15
        )

        self.voice_button.pack()

        # -----------------------------------------
        # STATUS
        # -----------------------------------------

        self.status = tk.Label(
            root,
            text="Ready",
            font=("Helvetica", 10),
            fg=self.secondary_text,
            bg=self.background_color
        )

        self.status.pack(
            pady=(0, 15)
        )

        # -----------------------------------------
        # INITIAL MESSAGE
        # -----------------------------------------

        self.add_message(
            "VISION",
            "VISION is online. How can I assist you?"
        )

        self.entry.focus()

    # =================================================
    # CHAT FUNCTIONS
    # =================================================

    def add_message(self, speaker, message):

        self.chat.configure(
            state="normal"
        )

        self.chat.insert(
            tk.END,
            f"{speaker}:\n",
        )

        self.chat.insert(
            tk.END,
            f"{message}\n\n"
        )

        self.chat.configure(
            state="disabled"
        )

        self.chat.see(
            tk.END
        )

    # =================================================
    # TEXT INPUT
    # =================================================

    def send_text(self, event=None):

        user_input = self.entry.get().strip()

        if not user_input:
            return

        self.entry.delete(
            0,
            tk.END
        )

        self.add_message(
            "You",
            user_input
        )

        self.set_status(
            "VISION is thinking..."
        )

        self.set_buttons(
            False
        )

        thread = threading.Thread(
            target=self.process_input,
            args=(user_input,),
            daemon=True
        )

        thread.start()

    # =================================================
    # VOICE INPUT
    # =================================================

    def start_voice(self):

        self.set_status(
            "Listening..."
        )

        self.set_buttons(
            False
        )

        thread = threading.Thread(
            target=self.process_voice,
            daemon=True
        )

        thread.start()

    def process_voice(self):

        try:

            if self.voice is None:

                self.voice = VoiceInput(
                    duration=5
                )

            user_input = self.voice.listen()

            if not user_input:

                self.root.after(
                    0,
                    self.voice_finished,
                    None
                )

                return

            self.root.after(
                0,
                self.voice_finished,
                user_input
            )

        except Exception as error:

            self.root.after(
                0,
                self.voice_error,
                str(error)
            )

    def voice_finished(self, user_input):

        if not user_input:

            self.set_status(
                "I didn't hear anything."
            )

            self.set_buttons(
                True
            )

            return

        self.add_message(
            "You",
            user_input
        )

        self.set_status(
            "VISION is thinking..."
        )

        thread = threading.Thread(
            target=self.process_input,
            args=(user_input,),
            daemon=True
        )

        thread.start()

    # =================================================
    # VISION PROCESSING
    # =================================================

    def process_input(self, user_input):

        try:

            response = self.vision.think(
                user_input
            )

            self.root.after(
                0,
                self.show_response,
                response
            )

        except Exception as error:

            self.root.after(
                0,
                self.show_response,
                f"An error occurred: {error}"
            )

    def show_response(self, response):

        self.add_message(
            "VISION",
            response
        )

        self.set_status(
            "Ready"
        )

        self.set_buttons(
            True
        )

        self.entry.focus()

    # =================================================
    # ERROR HANDLING
    # =================================================

    def voice_error(self, error):

        self.add_message(
            "VISION",
            f"Voice input error: {error}"
        )

        self.set_status(
            "Ready"
        )

        self.set_buttons(
            True
        )

    # =================================================
    # UI HELPERS
    # =================================================

    def set_status(self, text):

        self.status.config(
            text=text
        )

    def set_buttons(self, enabled):

        state = tk.NORMAL if enabled else tk.DISABLED

        self.send_button.config(
            state=state
        )

        self.voice_button.config(
            state=state
        )

        self.entry.config(
            state=state
        )


# =====================================================
# START APPLICATION
# =====================================================

def main():

    root = tk.Tk()

    app = VisionGUI(
        root
    )

    root.mainloop()


if __name__ == "__main__":

    main()