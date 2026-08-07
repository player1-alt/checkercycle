import tkinter as tk
from tkinter import ttk, filedialog
import json
import os


class CheckerCycleApp:

    def __init__(self, root):

        self.root = root

        self.root.title("CheckerCycle Renderer")
        self.root.geometry("520x650")
        self.root.resizable(False, False)

        self.settings_file = os.path.join(
            "config",
            "settings.json"
        )

        self.audio_map_file = os.path.join(
            "config",
            "audio_map.json"
        )

        self.create_widgets()
        self.load_settings()

    # ==========================
    # CREATE GUI
    # ==========================

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
            text="Browse...",
            command=self.browse_game
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

        self.base_interval = self.create_setting(
            timing_frame,
            "Base interval:",
            0
        )

        self.start_hold = self.create_setting(
            timing_frame,
            "Start hold:",
            1
        )

        self.hold_increase = self.create_setting(
            timing_frame,
            "Hold increase:",
            2
        )

        self.audio_move_hold = self.create_setting(
            timing_frame,
            "Audio move hold:",
            3
        )

        self.final_hold = self.create_setting(
            timing_frame,
            "Final hold:",
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
            text="Configure Audio Map",
            command=self.open_audio_map
        )

        self.audio_button.pack(
            padx=10,
            pady=15
        )

        # ==========================
        # SAVE SETTINGS
        # ==========================

        self.save_button = ttk.Button(
            self.root,
            text="SAVE SETTINGS",
            command=self.save_settings
        )

        self.save_button.pack(
            pady=(10, 5)
        )

        # ==========================
        # RENDER
        # ==========================

        self.render_button = ttk.Button(
            self.root,
            text="RENDER GAME",
            command=self.render_game
        )

        self.render_button.pack(
            pady=5
        )

        # ==========================
        # STATUS
        # ==========================

        self.status_label = ttk.Label(
            self.root,
            text="Status: Ready"
        )

        self.status_label.pack(
            pady=5
        )

    # ==========================
    # SETTING ENTRY
    # ==========================

    def create_setting(
        self,
        parent,
        label_text,
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

        entry.grid(
            row=row,
            column=1,
            sticky="w",
            padx=10,
            pady=5
        )

        return entry

    # ==========================
    # BROWSE GAME
    # ==========================

    def browse_game(self):

        filename = filedialog.askopenfilename(
            title="Select Checkers Game",
            filetypes=[
                ("Text files", "*.txt"),
                ("All files", "*.*")
            ]
        )

        if filename:

            self.game_file.delete(
                0,
                tk.END
            )

            self.game_file.insert(
                0,
                filename
            )

            self.status_label.config(
                text="Status: Game selected"
            )

    # ==========================
    # LOAD SETTINGS
    # ==========================

    def load_settings(self):

        try:

            with open(
                self.settings_file,
                "r"
            ) as file:

                settings = json.load(file)

            timeline = settings.get(
                "timeline",
                {}
            )

            audio = settings.get(
                "audio",
                {}
            )

            video = settings.get(
                "video",
                {}
            )

            self.set_entry(
                self.base_interval,
                timeline.get(
                    "base_interval",
                    2
                )
            )

            self.set_entry(
                self.start_hold,
                timeline.get(
                    "start_hold",
                    3
                )
            )

            self.set_entry(
                self.hold_increase,
                timeline.get(
                    "hold_increase",
                    2
                )
            )

            self.set_entry(
                self.audio_move_hold,
                audio.get(
                    "move_hold",
                    2
                )
            )

            self.set_entry(
                self.final_hold,
                video.get(
                    "final_hold",
                    settings.get(
                        "final_hold",
                        5
                    )
                )
            )

        except FileNotFoundError:

            self.status_label.config(
                text="Status: Settings file not found"
            )

        except json.JSONDecodeError:

            self.status_label.config(
                text="Status: Invalid settings.json"
            )

        except Exception:

            self.status_label.config(
                text="Status: Error loading settings"
            )

    # ==========================
    # SET ENTRY VALUE
    # ==========================

    def set_entry(
        self,
        entry,
        value
    ):

        entry.delete(
            0,
            tk.END
        )

        entry.insert(
            0,
            str(value)
        )

    # ==========================
    # SAVE SETTINGS
    # ==========================

    def save_settings(self):

        try:

            settings = {

                "initial_hold": self.get_number(
                    self.start_hold
                ),

                "final_hold": self.get_number(
                    self.final_hold
                ),

                "timeline": {

                    "base_interval": self.get_number(
                        self.base_interval
                    ),

                    "start_hold": self.get_number(
                        self.start_hold
                    ),

                    "hold_increase": self.get_number(
                        self.hold_increase
                    )
                },

                "audio": {

                    "move_hold": self.get_number(
                        self.audio_move_hold
                    )
                },

                "video": {

                    "position_hold_frames": 8,

                    "final_hold": self.get_number(
                        self.final_hold
                    )
                }
            }

            with open(
                self.settings_file,
                "w"
            ) as file:

                json.dump(
                    settings,
                    file,
                    indent=4
                )

            self.status_label.config(
                text="Status: Settings saved"
            )

        except ValueError:

            self.status_label.config(
                text="Status: Enter valid numbers"
            )

        except Exception:

            self.status_label.config(
                text="Status: Could not save settings"
            )

    # ==========================
    # GET NUMBER
    # ==========================

    def get_number(
        self,
        entry
    ):

        value = float(
            entry.get()
        )

        if value.is_integer():

            return int(value)

        return value

    # ==========================
    # RENDER GAME
    # ==========================

    def render_game(self):

        filename = self.game_file.get().strip()

        if not filename:

            self.status_label.config(
                text="Status: Select a game file"
            )

            return

        if not os.path.isfile(filename):

            self.status_label.config(
                text="Status: Game file not found"
            )

            return

        self.status_label.config(
            text="Status: Ready to render"
        )

        print(
            "Selected game:",
            filename
        )

    # ==========================
    # AUDIO MAP WINDOW
    # ==========================

    def open_audio_map(self):

        window = tk.Toplevel(
            self.root
        )

        window.title(
            "CheckerCycle - Audio Map"
        )

        window.geometry(
            "650x700"
        )

        window.resizable(
            False,
            False
        )

        ttk.Label(
            window,
            text="AUDIO MAP",
            font=("Arial", 18, "bold")
        ).pack(
            pady=(15, 5)
        )

        ttk.Label(
            window,
            text="Assign an MP3 file to each board square."
        ).pack(
            pady=(0, 10)
        )

        # ==========================
        # SCROLLABLE AREA
        # ==========================

        container = ttk.Frame(
            window
        )

        container.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=10
        )

        canvas = tk.Canvas(
            container
        )

        scrollbar = ttk.Scrollbar(
            container,
            orient="vertical",
            command=canvas.yview
        )

        scroll_frame = ttk.Frame(
            canvas
        )

        scroll_frame.bind(
            "<Configure>",
            lambda event: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window(
            (0, 0),
            window=scroll_frame,
            anchor="nw"
        )

        canvas.configure(
            yscrollcommand=scrollbar.set
        )

        canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        # ==========================
        # LOAD AUDIO MAP
        # ==========================

        audio_map = self.load_audio_map()

        audio_entries = {}

        # ==========================
        # 32 SQUARES
        # ==========================

        for square in range(1, 33):

            row = square - 1

            ttk.Label(
                scroll_frame,
                text=f"Square {square}:",
                width=12
            ).grid(
                row=row,
                column=0,
                padx=5,
                pady=4,
                sticky="w"
            )

            entry = ttk.Entry(
                scroll_frame,
                width=45
            )

            entry.grid(
                row=row,
                column=1,
                padx=5,
                pady=4
            )

            entry.insert(
                0,
                audio_map.get(
                    str(square),
                    ""
                )
            )

            audio_entries[square] = entry

            ttk.Button(
                scroll_frame,
                text="Browse",
                command=lambda e=entry: self.browse_audio(e)
            ).grid(
                row=row,
                column=2,
                padx=5,
                pady=4
            )

        # ==========================
        # SAVE BUTTON
        # ==========================

        ttk.Button(
            window,
            text="SAVE AUDIO MAP",
            command=lambda: self.save_audio_map(
                audio_entries,
                window
            )
        ).pack(
            pady=(5, 15)
        )

    # ==========================
    # LOAD AUDIO MAP
    # ==========================

    def load_audio_map(self):

        try:

            with open(
                self.audio_map_file,
                "r"
            ) as file:

                return json.load(file)

        except FileNotFoundError:

            return {}

        except json.JSONDecodeError:

            return {}

    # ==========================
    # BROWSE AUDIO
    # ==========================

    def browse_audio(
        self,
        entry
    ):

        filename = filedialog.askopenfilename(
            title="Select MP3",
            filetypes=[
                ("MP3 files", "*.mp3"),
                ("All files", "*.*")
            ]
        )

        if filename:

            entry.delete(
                0,
                tk.END
            )

            entry.insert(
                0,
                filename
            )

    # ==========================
    # SAVE AUDIO MAP
    # ==========================

    def save_audio_map(
        self,
        entries,
        window
    ):

        audio_map = {}

        for square in range(1, 33):

            audio_map[str(square)] = entries[
                square
            ].get()

        try:

            with open(
                self.audio_map_file,
                "w"
            ) as file:

                json.dump(
                    audio_map,
                    file,
                    indent=4
                )

            self.status_label.config(
                text="Status: Audio map saved"
            )

            window.destroy()

        except Exception:

            self.status_label.config(
                text="Status: Could not save audio map"
            )


def main():

    root = tk.Tk()

    app = CheckerCycleApp(
        root
    )

    root.mainloop()


if __name__ == "__main__":

    main()