import tkinter as tk
from tkinter import ttk, filedialog
import json
import os

from src.renderer.engine import RendererEngine


class CheckerCycleApp:


    def __init__(self, root):

        self.root = root

        self.root.title(
            "CheckerCycle Renderer"
        )

        self.root.geometry(
            "520x650"
        )

        self.root.resizable(
            False,
            False
        )


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
    def create_widgets(self):


        title = ttk.Label(
            self.root,
            text="CHECKERCYCLE",
            font=("Arial",20,"bold")
        )

        title.pack(
            pady=(20,5)
        )


        subtitle = ttk.Label(
            self.root,
            text="Checkers Variation Renderer"
        )

        subtitle.pack(
            pady=(0,20)
        )


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


        ttk.Button(
            game_frame,
            text="Browse...",
            command=self.browse_game
        ).grid(
            row=0,
            column=2,
            padx=10,
            pady=15
        )


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


        audio_frame = ttk.LabelFrame(
            self.root,
            text="AUDIO"
        )

        audio_frame.pack(
            fill="x",
            padx=25,
            pady=10
        )


        ttk.Button(
            audio_frame,
            text="Configure Audio Map",
            command=self.open_audio_map
        ).pack(
            pady=15
        )


        ttk.Button(
            self.root,
            text="SAVE SETTINGS",
            command=self.save_settings
        ).pack(
            pady=5
        )


        ttk.Button(
            self.root,
            text="RENDER GAME",
            command=self.render_game
        ).pack(
            pady=5
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
        row
    ):


        ttk.Label(
            parent,
            text=label_text
        ).grid(
            row=row,
            column=0,
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
            padx=10,
            pady=5
        )


        return entry



    def browse_game(self):


        filename = filedialog.askopenfilename(
            title="Select Checkers Game",
            filetypes=[
                ("Text files","*.txt"),
                ("All files","*.*")
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



    def load_settings(self):


        try:


            with open(
                self.settings_file,
                "r"
            ) as file:


                settings = json.load(
                    file
                )


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
                    5
                )
            )


        except FileNotFoundError:


            pass



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
    def save_settings(self):


        os.makedirs(
            "config",
            exist_ok=True
        )


        settings = {

            "timeline": {

                "base_interval":
                    self.get_number(
                        self.base_interval
                    ),

                "start_hold":
                    self.get_number(
                        self.start_hold
                    ),

                "hold_increase":
                    self.get_number(
                        self.hold_increase
                    )

            },


            "audio": {

                "move_hold":
                    self.get_number(
                        self.audio_move_hold
                    )

            },


            "video": {

                "final_hold":
                    self.get_number(
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
            text="Status: Rendering..."
        )


        self.root.update()



        try:


            engine = RendererEngine()


            engine.render(
                filename
            )


            self.status_label.config(
                text="Status: Render complete"
            )


        except Exception as e:


            print(
                "Render error:",
                e
            )


            self.status_label.config(
                text="Status: Render failed"
            )
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


        ttk.Label(
            window,
            text="AUDIO MAP",
            font=("Arial",18,"bold")
        ).pack(
            pady=15
        )


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
            lambda e:
                canvas.configure(
                    scrollregion=canvas.bbox("all")
                )
        )


        canvas.create_window(
            (0,0),
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


        audio_map = self.load_audio_map()


        entries = {}


        for square in range(1,33):


            ttk.Label(
                scroll_frame,
                text=f"Square {square}:",
                width=12
            ).grid(
                row=square,
                column=0,
                padx=5,
                pady=4
            )


            entry = ttk.Entry(
                scroll_frame,
                width=45
            )


            entry.grid(
                row=square,
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


            entries[square] = entry



            ttk.Button(
                scroll_frame,
                text="Browse",
                command=lambda e=entry:
                    self.browse_audio(e)
            ).grid(
                row=square,
                column=2,
                padx=5,
                pady=4
            )



        ttk.Button(
            window,
            text="SAVE AUDIO MAP",
            command=lambda:
                self.save_audio_map(
                    entries,
                    window
                )
        ).pack(
            pady=10
        )
    def load_audio_map(self):


        try:

            with open(
                self.audio_map_file,
                "r"
            ) as file:

                return json.load(file)


        except:

            return {}



    def browse_audio(
        self,
        entry
    ):


        filename = filedialog.askopenfilename(

            title="Select MP3",

            filetypes=[

                ("MP3 files","*.mp3"),

                ("All files","*.*")

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



    def save_audio_map(
        self,
        entries,
        window
    ):


        os.makedirs(
            "config",
            exist_ok=True
        )


        audio_map = {}


        for square in range(1,33):


            audio_map[str(square)] = entries[square].get()



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
def main():

    root = tk.Tk()

    app = CheckerCycleApp(
        root
    )

    root.mainloop()



if __name__ == "__main__":

    main()



