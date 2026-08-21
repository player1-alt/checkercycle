from pathlib import Path
import re
import sys


# ============================================================
# MOVE PATTERN
# ============================================================

MOVE_PATTERN = re.compile(
    r"\b\d{1,2}\s*(?:-|x)\s*\d{1,2}"
    r"(?:\s*(?:-|x|\|)\s*\d{1,2})*"
)


# ============================================================
# NUMBERED VARIATION DECLARATIONS
#
# V1(T):
# V5(4):
# V7(6):
# ============================================================

VARIATION_PATTERN = re.compile(
    r"\bV(\d+)\s*\((T|\d+)\)\s*:",
    re.IGNORECASE
)


# ============================================================
# HELPERS
# ============================================================

def clean_move(move):
    return re.sub(r"\s+", "", move)


def load_ballot(path):
    return Path(path).read_text(
        encoding="utf-8"
    )


# ============================================================
# FIND NUMBERED MARKERS
#
# Examples:
#
# 26-23[R](1)
# 12-16(5)
# 30-25(8)
#
# The marker belongs to THAT EXACT MOVE OCCURRENCE.
# ============================================================

def find_markers(text):
    markers = []

    for match in re.finditer(
        r"("
        r"\b\d{1,2}\s*(?:-|x)\s*\d{1,2}"
        r"(?:\s*(?:-|x|\|)\s*\d{1,2})*"
        r")"
        r"\s*(?:\[R\])?"
        r"\s*\((\d+)\)",
        text,
        re.IGNORECASE
    ):
        markers.append(
            {
                "move": clean_move(
                    match.group(1)
                ),
                "marker": int(
                    match.group(2)
                ),
                "start": match.start(1),
                "end": match.end(1)
            }
        )

    return markers


# ============================================================
# BRACKET PARSER
#
# [R] is NOT a branch.
#
# Real brackets become nodes.
# Nested brackets become child nodes.
# ============================================================

def parse_brackets(text):
    root = {
        "items": []
    }

    stack = [root]
    buffer = []

    def flush_text():
        nonlocal buffer

        if buffer:
            stack[-1]["items"].append(
                {
                    "type": "text",
                    "text": "".join(buffer)
                }
            )

        buffer = []

    i = 0

    while i < len(text):

        # ----------------------------------------------------
        # [R] IS ORDINARY TEXT
        # ----------------------------------------------------

        if text[i:i + 3].upper() == "[R]":
            buffer.extend(
                text[i:i + 3]
            )
            i += 3
            continue

        # ----------------------------------------------------
        # REAL OPEN BRACKET
        # ----------------------------------------------------

        if text[i] == "[":
            flush_text()

            node = {
                "items": []
            }

            stack[-1]["items"].append(
                {
                    "type": "bracket",
                    "node": node
                }
            )

            stack.append(node)
            i += 1
            continue

        # ----------------------------------------------------
        # CLOSE BRACKET
        # ----------------------------------------------------

        if text[i] == "]":
            flush_text()

            if len(stack) > 1:
                stack.pop()
            else:
                buffer.append("]")

            i += 1
            continue

        buffer.append(
            text[i]
        )

        i += 1

    flush_text()

    return root


# ============================================================
# MOVES FROM TEXT
# ============================================================

def extract_moves(text):
    return [
        clean_move(match.group(0))
        for match in MOVE_PATTERN.finditer(text)
    ]


# ============================================================
# GET DIRECT MOVES FROM A BRACKET NODE
#
# Nested bracket contents are excluded.
# ============================================================

def direct_moves(node):
    moves = []

    for item in node["items"]:

        if item["type"] == "text":
            moves.extend(
                extract_moves(
                    item["text"]
                )
            )

    return moves


# ============================================================
# SPLIT NUMBERED VARIATIONS
# ============================================================

def split_variations(text):

    declarations = list(
        VARIATION_PATTERN.finditer(text)
    )

    sections = []

    # --------------------------------------------------------
    # No V declarations
    # --------------------------------------------------------

    if not declarations:

        sections.append(
            {
                "name": "T",
                "parent": None,
                "text": text
            }
        )

        return sections

    # --------------------------------------------------------
    # TRUNK
    # --------------------------------------------------------

    sections.append(
        {
            "name": "T",
            "parent": None,
            "text": text[
                :declarations[0].start()
            ]
        }
    )

    # --------------------------------------------------------
    # V SECTIONS
    # --------------------------------------------------------

    for i, declaration in enumerate(
        declarations
    ):

        number = int(
            declaration.group(1)
        )

        parent = declaration.group(2)

        start = declaration.end()

        if i + 1 < len(declarations):
            end = declarations[
                i + 1
            ].start()
        else:
            end = len(text)

        sections.append(
            {
                "name": f"V{number}",
                "parent": (
                    "T"
                    if parent.upper() == "T"
                    else f"V{parent}"
                ),
                "text": text[
                    start:end
                ]
            }
        )

    return sections


# ============================================================
# BUILD VARIATION MAP
# ============================================================

def build_variation_map(sections):

    result = {}

    for section in sections:

        result[
            section["name"]
        ] = {
            "name": section["name"],
            "parent": section["parent"],
            "text": section["text"]
        }

    return result


# ============================================================
# FIND EXACT MARKER IN A SECTION
#
# IMPORTANT:
# We record the marker's MOVE INDEX while parsing the section.
#
# The move text is NOT used as a unique identifier.
# ============================================================

def marker_positions(text):

    """
    Find numbered markers on the DIRECT/main line only.

    Moves inside [ ... ] are separate variations and must
    NOT affect the move index of markers on the parent line.
    """

    root = parse_brackets(text)

    result = []
    move_index = 0

    for item in root["items"]:

        # ----------------------------------------------------
        # ONLY PROCESS DIRECT TEXT
        #
        # Do NOT recurse into brackets.
        # ----------------------------------------------------

        if item["type"] != "text":
            continue

        text_part = item["text"]

        moves = list(
            MOVE_PATTERN.finditer(
                text_part
            )
        )

        markers = list(
            re.finditer(
                r"\b"
                r"\d{1,2}\s*(?:-|x)\s*\d{1,2}"
                r"(?:\s*(?:-|x|\|)\s*\d{1,2})*"
                r"\s*(?:\[R\])?"
                r"\s*\((\d+)\)",
                text_part,
                re.IGNORECASE
            )
        )

        for move_match in moves:

            move = clean_move(
                move_match.group(0)
            )

            marker_number = None

            for marker_match in markers:

                # The marker must belong to THIS exact move.
                if (
                    marker_match.start()
                    == move_match.start()
                ):
                    marker_number = int(
                        marker_match.group(1)
                    )
                    break

            if marker_number is not None:

                result.append(
                    {
                        "marker": marker_number,
                        "move": move,
                        "index": move_index
                    }
                )

            move_index += 1

    return result


# ============================================================
# RESOLVE NUMBERED BRANCHES
# ============================================================

def resolve_numbered_branches(
    variation_map
):

    for name, info in (
        variation_map.items()
    ):

        if name == "T":
            continue

        parent = info["parent"]

        parent_info = variation_map.get(
            parent
        )

        if parent_info is None:

            info["branch_marker"] = None
            info["branch_index"] = None
            info["branch_move"] = None

            continue

        number = int(
            name[1:]
        )

        # ----------------------------------------------------
        # The marker belongs to the PARENT.
        # ----------------------------------------------------

        parent_markers = marker_positions(
            parent_info["text"]
        )

        matches = [
            m
            for m in parent_markers
            if m["marker"] == number
        ]

        if not matches:

            info["branch_marker"] = number
            info["branch_index"] = None
            info["branch_move"] = None

            print(
                f"WARNING: {name}: "
                f"marker ({number}) was not found "
                f"in {parent}."
            )

            continue

        marker = matches[0]

        info["branch_marker"] = number

        # IMPORTANT:
        #
        # This is the marker's index inside the
        # parent's LOCAL section.
        #
        # build_numbered_game() converts it to an
        # absolute index inside the parent's complete game.

        info["branch_index"] = (
            marker["index"]
        )

        info["branch_move"] = (
            marker["move"]
        )


# ============================================================
# GET THE MAIN-LINE MOVES OF A SECTION
#
# Bracket contents are excluded.
# ============================================================

def section_main_moves(text):

    root = parse_brackets(text)

    return direct_moves(root)


# ============================================================
# BUILD NUMBERED GAME
#
# THIS SECTION IS THE ORIGINAL WORKING NUMBERED-VARIATION
# LOGIC. DO NOT CHANGE.
# ============================================================

def build_numbered_game(
    name,
    variation_map,
    cache
):

    if name in cache:
        return cache[name]

    info = variation_map[name]

    # --------------------------------------------------------
    # TRUNK
    # --------------------------------------------------------

    if name == "T":

        game = section_main_moves(
            info["text"]
        )

        cache[name] = game

        return game

    # --------------------------------------------------------
    # BUILD COMPLETE PARENT FIRST
    # --------------------------------------------------------

    parent_name = info["parent"]

    parent_game = build_numbered_game(
        parent_name,
        variation_map,
        cache
    )

    branch_index = info[
        "branch_index"
    ]

    # --------------------------------------------------------
    # NO MARKER
    # --------------------------------------------------------

    if branch_index is None:

        print(
            f"WARNING: {name} cannot be "
            f"placed into {parent_name}."
        )

        game = (
            parent_game
            + section_main_moves(
                info["text"]
            )
        )

        cache[name] = game

        return game

    # --------------------------------------------------------
    # IMPORTANT FIX
    #
    # branch_index is LOCAL to the parent's section.
    #
    # parent_game is the COMPLETE reconstructed
    # parent game.
    #
    # Therefore we must add the number of moves
    # inherited by the parent before its own section.
    # --------------------------------------------------------

    parent_local_moves = section_main_moves(
        variation_map[parent_name]["text"]
    )

    inherited_length = (
        len(parent_game)
        - len(parent_local_moves)
    )

    absolute_branch_index = (
        inherited_length
        + branch_index
    )

    # --------------------------------------------------------
    # CHILD'S OWN MAIN LINE
    # --------------------------------------------------------

    child_moves = section_main_moves(
        info["text"]
    )

    # --------------------------------------------------------
    # REPLACE THE MARKED MOVE
    #
    # The marked move itself is discarded.
    # Everything after it in parent is discarded.
    # --------------------------------------------------------

    prefix = parent_game[
        :absolute_branch_index
    ]

    game = (
        prefix
        + child_moves
    )

    cache[name] = game

    return game


# ============================================================
# BRACKET VARIATION EXTRACTION
#
# BRACKETS ARE TREATED LIKE NUMBERED VARIATIONS.
#
# A bracket variation has:
#
#   parent
#   branch_index
#   branch_move
#   own moves
#
# Example:
#
# T:
# A B C D E F G
#
#      [ X Y Z ]
#
# If the bracket follows D:
#
# B1 = A B C X Y Z
#
# NOT:
#
# B1 = D X Y Z
#
# The complete parent game is reconstructed first.
# ============================================================


# ============================================================
# GET DIRECT ITEMS OF A NODE
# ============================================================

def node_direct_items(node):
    return [
        item
        for item in node["items"]
    ]


# ============================================================
# FIND ALL BRACKETS IN A TEXT SECTION
#
# Each bracket becomes a variation-like record.
#
# The parent is the variation whose text contains the bracket.
#
# For example:
#
# T  -> B1
# V2 -> B2
# V3 -> B3
# B1 -> B4
# ============================================================

def find_bracket_variations(
    text,
    parent_name,
    counter
):

    root = parse_brackets(text)

    results = []

    # --------------------------------------------------------
    # Walk only this section.
    #
    # Nested brackets are discovered recursively.
    # --------------------------------------------------------

    def walk(
        node,
        direct_history,
        current_parent
    ):

        history = list(
            direct_history
        )

        for item in node["items"]:

            # ------------------------------------------------
            # NORMAL TEXT
            # ------------------------------------------------

            if item["type"] == "text":

                history.extend(
                    extract_moves(
                        item["text"]
                    )
                )

                continue

            # ------------------------------------------------
            # BRACKET
            # ------------------------------------------------

            child = item["node"]

            # The bracket replaces the move immediately
            # before its opening bracket.
            branch_index = (
                len(history) - 1
            )

            branch_move = (
                history[-1]
                if history
                else None
            )

            # ------------------------------------------------
            # Direct moves belonging to this bracket.
            #
            # Nested bracket moves are excluded.
            # ------------------------------------------------

            child_moves = direct_moves(
                child
            )

            counter[0] += 1

            name = (
                f"B{counter[0]}"
            )

            results.append(
                {
                    "name": name,
                    "parent": current_parent,
                    "branch_index": branch_index,
                    "branch_move": branch_move,
                    "moves": child_moves
                }
            )

            # ------------------------------------------------
            # IMPORTANT:
            #
            # Nested brackets belong to THIS bracket.
            #
            # The history entering the child consists of
            # the parent history BEFORE the outer bracket,
            # followed by the OUTER bracket's direct moves
            # processed up to the nested bracket.
            #
            # This makes:
            #
            # T + V2 + B1 + B2
            #
            # work naturally.
            # ------------------------------------------------

            child_history = list(
                history[:-1]
                if history
                else []
            )

            walk(
                child,
                child_history,
                name
            )

            # ------------------------------------------------
            # The parent/main line continues after the bracket.
            #
            # Therefore DO NOT modify `history`.
            # ------------------------------------------------

    walk(
        root,
        [],
        parent_name
    )

    return results


# ============================================================
# BUILD ONE BRACKET GAME
#
# This deliberately mirrors build_numbered_game().
#
# Parent:
#
#     T
#     V2
#     V3
#     B1
#
# is fully reconstructed first.
#
# Then the bracket branch point is applied.
# ============================================================

def build_bracket_game(
    name,
    bracket_map,
    variation_map,
    numbered_cache,
    bracket_cache
):

    if name in bracket_cache:
        return bracket_cache[name]

    info = bracket_map[name]

    parent_name = info["parent"]

    # --------------------------------------------------------
    # BUILD COMPLETE PARENT
    # --------------------------------------------------------

    if parent_name in bracket_map:

        parent_game = build_bracket_game(
            parent_name,
            bracket_map,
            variation_map,
            numbered_cache,
            bracket_cache
        )

    else:

        parent_game = build_numbered_game(
            parent_name,
            variation_map,
            numbered_cache
        )

    # --------------------------------------------------------
    # BRANCH INDEX IS LOCAL TO THE PARENT SECTION.
    #
    # For a bracket inside V2, the index is based on V2's
    # own local moves.
    #
    # For a bracket inside B1, the index is based on B1's
    # own bracket continuation.
    # --------------------------------------------------------

    branch_index = info[
        "branch_index"
    ]

    # --------------------------------------------------------
    # Determine how many inherited moves exist before the
    # parent's own local section.
    #
    # This mirrors build_numbered_game().
    # --------------------------------------------------------

    if parent_name in bracket_map:

        parent_local_length = len(
            bracket_map[parent_name]["moves"]
        )

    else:

        parent_local_length = len(
            section_main_moves(
                variation_map[parent_name]["text"]
            )
        )

    inherited_length = (
        len(parent_game)
        - parent_local_length
    )

    absolute_branch_index = (
        inherited_length
        + branch_index
    )

    # --------------------------------------------------------
    # Replace the branch move.
    #
    # Everything from the branch move onward in the parent
    # is discarded.
    # --------------------------------------------------------

    prefix = parent_game[
        :absolute_branch_index
    ]

    branch_moves = info[
        "moves"
    ]

    game = (
        prefix
        + branch_moves
    )

    bracket_cache[name] = game

    return game


# ============================================================
# BUILD BRACKET MAP
# ============================================================

def build_bracket_map(
    sections,
    variation_map
):

    bracket_map = {}

    counter = [0]

    # --------------------------------------------------------
    # IMPORTANT:
    #
    # Brackets are found independently inside EVERY section.
    #
    # T
    # V1
    # V2
    # V3
    #
    # This means a bracket in V3 has parent V3, not T.
    # --------------------------------------------------------

    for section in sections:

        section_brackets = (
            find_bracket_variations(
                section["text"],
                section["name"],
                counter
            )
        )

        for bracket in section_brackets:

            bracket_map[
                bracket["name"]
            ] = bracket

    return bracket_map


# ============================================================
# BUILD ALL GAMES
# ============================================================

def build_all_games(
    sections,
    variation_map
):

    complete_games = {}

    numbered_cache = {}

    # --------------------------------------------------------
    # FIRST:
    #
    # Build all numbered variations exactly as before.
    # --------------------------------------------------------

    for section in sections:

        name = section["name"]

        complete_games[name] = (
            build_numbered_game(
                name,
                variation_map,
                numbered_cache
            )
        )

    # --------------------------------------------------------
    # SECOND:
    #
    # Discover all bracket variations.
    # --------------------------------------------------------

    bracket_map = build_bracket_map(
        sections,
        variation_map
    )

    bracket_cache = {}

    # --------------------------------------------------------
    # THIRD:
    #
    # Build each bracket exactly like a numbered variation.
    #
    # A bracket can itself be the parent of another bracket.
    # --------------------------------------------------------

    for name in bracket_map:

        complete_games[name] = (
            build_bracket_game(
                name,
                bracket_map,
                variation_map,
                numbered_cache,
                bracket_cache
            )
        )

    return complete_games


# ============================================================
# OUTPUT
# ============================================================

def write_game(
    output_dir,
    name,
    moves
):

    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    path = (
        output_dir
        / f"{name}.txt"
    )

    path.write_text(
        " ".join(moves)
        + "\n",
        encoding="utf-8"
    )

    print(
        f"Written: {path}"
    )


def write_all_games(
    complete_games,
    output_dir
):

    print()
    print(
        "=== WRITING COMPLETE GAMES ==="
    )

    for name, moves in (
        complete_games.items()
    ):

        write_game(
            output_dir,
            name,
            moves
        )


# ============================================================
# DISPLAY VARIATION MAP
# ============================================================

def print_variation_map(
    variation_map
):

    print()
    print(
        "=== VARIATION MAP ==="
    )

    for name, info in (
        variation_map.items()
    ):

        if name == "T":

            print("T")

            continue

        print()
        print(name)

        print(
            f"  parent: "
            f"{info['parent']}"
        )

        print(
            f"  marker: "
            f"({info['branch_marker']})"
        )

        print(
            f"  branch move: "
            f"{info['branch_move']}"
        )

        print(
            f"  branch index: "
            f"{info['branch_index']}"
        )


# ============================================================
# DISPLAY BRACKET MAP
# ============================================================

def print_bracket_map(
    bracket_map
):

    print()
    print(
        "=== BRACKET MAP ==="
    )

    if not bracket_map:

        print(
            "No bracket variations found."
        )

        return

    for name, info in (
        bracket_map.items()
    ):

        print()
        print(name)

        print(
            f"  parent: "
            f"{info['parent']}"
        )

        print(
            f"  branch move: "
            f"{info['branch_move']}"
        )

        print(
            f"  branch index: "
            f"{info['branch_index']}"
        )

        print(
            f"  bracket moves: "
            f"{len(info['moves'])}"
        )


# ============================================================
# DISPLAY GAMES
# ============================================================

def print_complete_games(
    complete_games
):

    print()
    print(
        "=== COMPLETE GAME PREVIEW ==="
    )

    for name, moves in (
        complete_games.items()
    ):

        print()
        print(
            f"{name}: {len(moves)} moves"
        )

        print(
            " ".join(moves)
        )


# ============================================================
# MAIN
# ============================================================

def main():

    if len(sys.argv) != 2:

        print(
            "Usage:"
        )

        print(
            "py src\\variation_extractor.py "
            "<ballot.txt>"
        )

        return

    input_path = Path(
        sys.argv[1]
    )

    text = load_ballot(
        input_path
    )

    # --------------------------------------------------------
    # SPLIT T / V1 / V2 / ...
    # --------------------------------------------------------

    sections = split_variations(
        text
    )

    # --------------------------------------------------------
    # BUILD NUMBERED VARIATION MAP
    # --------------------------------------------------------

    variation_map = (
        build_variation_map(
            sections
        )
    )

    # --------------------------------------------------------
    # RESOLVE NUMBERED MARKERS
    #
    # UNCHANGED.
    # --------------------------------------------------------

    resolve_numbered_branches(
        variation_map
    )

    print_variation_map(
        variation_map
    )

    # --------------------------------------------------------
    # BUILD ALL COMPLETE GAMES
    # --------------------------------------------------------

    complete_games = (
        build_all_games(
            sections,
            variation_map
        )
    )

    # --------------------------------------------------------
    # BUILD BRACKET MAP FOR DISPLAY
    # --------------------------------------------------------

    bracket_map = build_bracket_map(
        sections,
        variation_map
    )

    print_bracket_map(
        bracket_map
    )

    # --------------------------------------------------------
    # DISPLAY
    # --------------------------------------------------------

    print_complete_games(
        complete_games
    )

    # --------------------------------------------------------
    # WRITE
    # --------------------------------------------------------

    output_dir = (
        input_path.parent
        / "output"
    )

    write_all_games(
        complete_games,
        output_dir
    )

    print()
    print(
        "=== DONE ==="
    )

    print(
        f"Total games: "
        f"{len(complete_games)}"
    )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()