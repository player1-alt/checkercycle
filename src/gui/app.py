import tkinter as tk
from tkinter import ttk


class CheckerCycleApp:

    def __init__(self, root):

        self.root = root

        self.root.title("CheckerCycle Renderer")
        self.root.geometry("520x500")
        self.root.resizable(False, False)

        self.create_widgets()

    def create_widgets(self):

        # ==========================
        # TITLE
        # ==========================

        title = ttk.Label(
            self.root,
            text="CHECKERCYCLE",
            font=("Arial", 20, "bold")
        )

        title.pack(pady=(20, 5))

        subtitle = ttk.Label(
            self.root,
            text="Checkers Variation Renderer"
        )

        subtitle.pack(pady=(0, 20))

        # ==========================
        # GAME FILE
        # ==========================

        game_frame = ttk.LabelFrame(
            self.root,
            text="GAME"
        )

        game_frame.pack(
            fill="x",
            padx=25,
            pady=10
        )

        ttk.Label(
            game_frame,
            text="Game file:"
        ).grid(
            row=0,
            column=0,
            padx=10,
            pady=15
        )

        self.game_file = ttk.Entry(
            game_frame,
            width=40
        )

        self.game_file.grid(
            row=0,
            column=1,
            padx=5,
            pady=15
        )

        self.browse_button = ttk.Button(
            game_frame,
            text="Browse..."
        )

        self.browse_button.grid(
            row=0,
            column=2,
            padx=10,
            pady=15
        )

        # ==========================
        # TIMING
        # ==========================

        timing_frame = ttk.LabelFrame(
            self.root,
            text="TIMING"
        )

        timing_frame.pack(
            fill="x",
            padx=25,
            pady=10
        )

        self.create_setting(
            timing_frame,
            "Base interval:",
            "2.0",
            0
        )

        self.create_setting(
            timing_frame,
            "Start hold:",
            "3.0",
            1
        )

        self.create_setting(
            timing_frame,
            "Hold increase:",
            "2.0",
            2
        )

        self.create_setting(
            timing_frame,
            "Audio move hold:",
            "2.0",
            3
        )

        self.create_setting(
            timing_frame,
            "Final hold:",
            "5.0",
            4
        )

        # ==========================
        # AUDIO
        # ==========================

        audio_frame = ttk.LabelFrame(
            self.root,
            text="AUDIO"
        )

        audio_frame.pack(
            fill="x",
            padx=25,
            pady=10
        )

        self.audio_button = ttk.Button(
            audio_frame,
            text="Configure Audio Map"
        )

        self.audio_button.pack(
            padx=10,
            pady=15
        )

        # ==========================
        # RENDER
        # ==========================

        self.render_button = ttk.Button(
            self.root,
            text="RENDER GAME"
        )

        self.render_button.pack(
            pady=(15, 5)
        )

        self.status_label = ttk.Label(
            self.root,
            text="Status: Ready"
        )

        self.status_label.pack(
            pady=5
        )

    def create_setting(
        self,
        parent,
        label_text,
        default_value,
        row
    ):

        ttk.Label(
            parent,
            text=label_text
        ).grid(
            row=row,
            column=0,
            sticky="w",
            padx=15,
            pady=5
        )

        entry = ttk.Entry(
            parent,
            width=10
        )

        entry.insert(
            0,
            default_value
        )

        entry.grid(
            row=row,
            column=1,
            sticky="w",
            padx=10,
            pady=5
        )


def main():

    root = tk.Tk()

    app = CheckerCycleApp(root)

    root.mainloop()


if __name__ == "__main__":
    main()
