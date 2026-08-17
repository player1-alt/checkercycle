import os


class NamingNode:
    """
    Simple CheckerCycle naming node.

    Takes the TXT filename and uses its base name
    for the six generated audio/video files.

    Example:

        ballot1 trunk.txt

    becomes:

        ballot1 trunk 13s.mp4
        ballot1 trunk 8s.mp4
        ballot1 trunk 4s.mp4

        ballot1 trunk 13s.mp3
        ballot1 trunk 8s.mp3
        ballot1 trunk 4s.mp3

    IMPORTANT:

    The original TXT file is never moved, renamed,
    copied, or deleted.

    Generated files are taken from and written to
    the CheckerCycle project directory.
    """

    def __init__(self):

        print("Naming Node loaded")

    # =========================================================
    # RENAME OUTPUTS
    # =========================================================

    def rename_outputs(self, game_file):

        # -----------------------------------------------------
        # PROJECT DIRECTORY
        #
        # Video and audio outputs are created in the
        # current CheckerCycle project directory.
        # -----------------------------------------------------

        directory = os.getcwd()

        # -----------------------------------------------------
        # Get TXT filename without extension
        #
        # The TXT itself can be anywhere.
        # We only use its filename for naming.
        # -----------------------------------------------------

        base_name = os.path.splitext(
            os.path.basename(game_file)
        )[0]

        print()
        print("=====================")
        print("NAMING OUTPUTS")
        print("=====================")

        print(
            "Base name:",
            base_name
        )

        print(
            "Output directory:",
            directory
        )

        # -----------------------------------------------------
        # Timeline modes
        # -----------------------------------------------------

        modes = [13, 8, 4]

        renamed_files = []

        # =====================================================
        # VIDEO
        # =====================================================

        for mode in modes:

            old_name = (
                f"CheckerCycle_{mode}s.mp4"
            )

            new_name = (
                f"{base_name} {mode}s.mp4"
            )

            old_path = os.path.join(
                directory,
                old_name
            )

            new_path = os.path.join(
                directory,
                new_name
            )

            self._rename(
                old_path,
                new_path
            )

            if os.path.exists(new_path):

                renamed_files.append(
                    new_path
                )

        # =====================================================
        # AUDIO
        # =====================================================

        for mode in modes:

            old_name = (
                f"CheckerCycle_audio_{mode}s.mp3"
            )

            new_name = (
                f"{base_name} {mode}s.mp3"
            )

            old_path = os.path.join(
                directory,
                old_name
            )

            new_path = os.path.join(
                directory,
                new_name
            )

            self._rename(
                old_path,
                new_path
            )

            if os.path.exists(new_path):

                renamed_files.append(
                    new_path
                )

        # =====================================================
        # REPORT
        # =====================================================

        print()
        print("=====================")
        print("NAMING COMPLETE")
        print("=====================")

        for path in renamed_files:

            print(
                os.path.basename(path)
            )

        print()

        return renamed_files

    # =========================================================
    # RENAME ONE FILE
    # =========================================================

    def _rename(
        self,
        old_path,
        new_path
    ):

        # -----------------------------------------------------
        # Source does not exist
        # -----------------------------------------------------

        if not os.path.exists(old_path):

            print(
                "Missing:",
                os.path.basename(old_path)
            )

            return

        # -----------------------------------------------------
        # Destination already exists
        #
        # This allows us to re-render the same TXT later.
        # -----------------------------------------------------

        if os.path.exists(new_path):

            os.remove(
                new_path
            )

        # -----------------------------------------------------
        # Rename
        # -----------------------------------------------------

        os.rename(
            old_path,
            new_path
        )

        print(
            "Renamed:",
            os.path.basename(old_path),
            "->",
            os.path.basename(new_path)
        )