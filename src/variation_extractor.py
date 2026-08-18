from pathlib import Path
import re
import sys


# ============================================================
# MOVE / VARIATION PATTERNS
# ============================================================

MOVE_PATTERN = re.compile(
    r"\b\d{1,2}\s*(?:-|x)\s*\d{1,2}"
    r"(?:\s*(?:-|x|\|)\s*\d{1,2})*"
)

VARIATION_PATTERN = re.compile(
    r"\bV(\d+)\((T|\d+)\)\s*:",
    re.IGNORECASE,
)

MARKER_PATTERN = re.compile(
    r"(\d{1,2}\s*(?:-|x)\s*\d{1,2}"
    r"(?:\s*(?:-|x|\|)\s*\d{1,2})*)"
    r"(?:\s*\[[^\]]*\])?"
    r"\s*\((\d+)\)"
)


# ============================================================
# BASIC HELPERS
# ============================================================

def load_ballot(path):
    return Path(path).read_text(
        encoding="utf-8"
    )


def clean_move(move):
    return re.sub(r"\s+", "", move)


def extract_moves(text):
    return [
        clean_move(m)
        for m in MOVE_PATTERN.findall(text)
    ]


# ============================================================
# NUMBERED VARIATION MARKERS
# ============================================================

def find_markers(text):

    markers = []

    for match in MARKER_PATTERN.finditer(text):

        move = clean_move(
            match.group(1)
        )

        marker = int(
            match.group(2)
        )

        markers.append(
            {
                "marker": marker,
                "move": move,
            }
        )

    return markers


# ============================================================
# SPLIT V SECTIONS
# ============================================================

def split_variations(text):

    declarations = list(
        VARIATION_PATTERN.finditer(text)
    )

    sections = []

    if declarations:

        sections.append(
            {
                "name": "T",
                "parent": None,
                "text": text[
                    :declarations[0].start()
                ],
            }
        )

        for i, match in enumerate(
            declarations
        ):

            number = match.group(1)
            parent = match.group(2)

            start = match.end()

            if i + 1 < len(declarations):

                end = declarations[
                    i + 1
                ].start()

            else:

                end = len(text)

            sections.append(
                {
                    "name": f"V{number}",
                    "parent": parent,
                    "text": text[start:end],
                }
            )

    else:

        sections.append(
            {
                "name": "T",
                "parent": None,
                "text": text,
            }
        )

    return sections


# ============================================================
# VARIATION MAP
# ============================================================

def build_variation_map(sections):

    variation_map = {}

    for section in sections:

        name = section["name"]
        parent = section["parent"]

        if name == "T":

            variation_map["T"] = {
                "name": "T",
                "parent": None,
                "text": section["text"],
            }

        else:

            if parent == "T":

                parent_name = "T"

            else:

                parent_name = f"V{parent}"

            variation_map[name] = {
                "name": name,
                "parent": parent_name,
                "text": section["text"],
            }

    return variation_map


# ============================================================
# RESOLVE NUMBERED VARIATION BRANCH POINTS
# ============================================================

def resolve_branch_points(
    variation_map
):

    for name, info in variation_map.items():

        if name == "T":
            continue

        parent = info["parent"]

        parent_info = variation_map.get(
            parent
        )

        if parent_info is None:

            info["marker"] = None
            info["branch_move"] = None

            continue

        number = int(
            name[1:]
        )

        parent_markers = find_markers(
            parent_info["text"]
        )

        matches = [
            marker
            for marker in parent_markers
            if marker["marker"] == number
        ]

        info["marker"] = number

        if matches:

            info["branch_move"] = (
                matches[0]["move"]
            )

        else:

            info["branch_move"] = None


# ============================================================
# BRACKET TREE
# ============================================================

def parse_bracket_tree(text):

    """
    Parse real square-bracket variations.

    IMPORTANT:

        [R]

    is a notation marker, NOT a variation.

    Therefore [R] is treated as ordinary text and
    does not create a bracket node.

    Nested real brackets are still preserved.
    """

    root = {
        "items": []
    }

    stack = [root]

    text_buffer = []

    def flush_text():

        nonlocal text_buffer

        if text_buffer:

            stack[-1]["items"].append(
                (
                    "text",
                    "".join(text_buffer)
                )
            )

            text_buffer = []

    i = 0

    while i < len(text):

        # ----------------------------------------------------
        # IGNORE [R] MARKERS
        # ----------------------------------------------------

        if text[i:i + 3].upper() == "[R]":

            text_buffer.extend(
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
                (
                    "bracket",
                    node
                )
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

                stack[-1]["items"].append(
                    (
                        "text",
                        "]"
                    )
                )

            i += 1
            continue

        # ----------------------------------------------------
        # NORMAL CHARACTER
        # ----------------------------------------------------

        text_buffer.append(
            text[i]
        )

        i += 1

    flush_text()

    return root


# ============================================================
# DIRECT MOVES OF A BRACKET NODE
# ============================================================

def extract_direct_moves(node):

    """
    Return only moves belonging directly to this node.

    Nested bracket contents are ignored.
    """

    moves = []

    for item_type, value in node["items"]:

        if item_type == "text":

            moves.extend(
                extract_moves(value)
            )

    return moves


# ============================================================
# DIRECT MOVES OF A SECTION
# ============================================================

def get_section_direct_moves(text):

    tree = parse_bracket_tree(
        text
    )

    return extract_direct_moves(
        tree
    )


# ============================================================
# FIND LAST MATCHING MOVE
# ============================================================

def find_last_matching_move(
    moves,
    target
):

    for i in range(
        len(moves) - 1,
        -1,
        -1
    ):

        if moves[i] == target:
            return i

    return None


# ============================================================
# NUMBERED VARIATION COMPLETE-GAME BUILDER
# ============================================================

def build_numbered_game(
    name,
    variation_map,
    cache=None
):

    if cache is None:
        cache = {}

    if name in cache:
        return cache[name]

    info = variation_map[name]

    # --------------------------------------------------------
    # TRUNK
    # --------------------------------------------------------

    if name == "T":

        moves = get_section_direct_moves(
            info["text"]
        )

        cache[name] = moves

        return moves

    # --------------------------------------------------------
    # PARENT
    # --------------------------------------------------------

    parent_name = info["parent"]

    parent_moves = build_numbered_game(
        parent_name,
        variation_map,
        cache
    )

    branch_move = info["branch_move"]

    own_moves = get_section_direct_moves(
        info["text"]
    )

    # --------------------------------------------------------
    # NO MARKER
    # --------------------------------------------------------

    if branch_move is None:

        result = (
            parent_moves
            + own_moves
        )

        cache[name] = result

        return result

    # --------------------------------------------------------
    # FIND BRANCH MOVE
    # --------------------------------------------------------

    branch_index = find_last_matching_move(
        parent_moves,
        branch_move
    )

    if branch_index is None:

        print(
            f"WARNING: {name}: "
            f"branch move {branch_move} "
            f"not found in parent game."
        )

        result = (
            parent_moves
            + own_moves
        )

        cache[name] = result

        return result

    # --------------------------------------------------------
    # REPLACE BRANCH MOVE
    # --------------------------------------------------------

    prefix = parent_moves[
        :branch_index
    ]

    result = (
        prefix
        + own_moves
    )

    cache[name] = result

    return result


# ============================================================
# BRACKET VARIATIONS
# ============================================================

def extract_all_bracket_games(
    section_text,
    base_history,
    section_name,
    counter
):

    root = parse_bracket_tree(
        section_text
    )

    results = []

    walk_node_for_brackets(
        root,
        list(base_history),
        results,
        counter,
        section_name
    )

    return results


def walk_node_for_brackets(
    node,
    history_before_node,
    results,
    counter,
    parent_name
):

    current_history = list(
        history_before_node
    )

    for item_type, value in node["items"]:

        # ----------------------------------------------------
        # NORMAL TEXT
        # ----------------------------------------------------

        if item_type == "text":

            current_history.extend(
                extract_moves(value)
            )

            continue

        # ----------------------------------------------------
        # REAL BRACKET
        # ----------------------------------------------------

        child = value

        bracket_start_history = list(
            current_history
        )

        child_direct_moves = (
            extract_direct_moves(
                child
            )
        )

        # ----------------------------------------------------
        # ONLY CREATE A GAME IF THE BRACKET
        # ACTUALLY CONTAINS MOVES
        # ----------------------------------------------------

        if child_direct_moves:

            counter[0] += 1

            bracket_name = (
                f"B{counter[0]}"
            )

            bracket_game = (
                bracket_start_history
                + child_direct_moves
            )

            results.append(
                {
                    "name": bracket_name,
                    "parent": parent_name,
                    "moves": bracket_game,
                }
            )

            # ------------------------------------------------
            # NESTED BRACKETS
            # ------------------------------------------------

            walk_node_for_brackets(
                child,
                bracket_game,
                results,
                counter,
                bracket_name
            )

        else:

            # ------------------------------------------------
            # EMPTY BRACKET
            #
            # Should normally not happen now except for
            # unusual malformed notation.
            # Do NOT create a game.
            # ------------------------------------------------

            walk_node_for_brackets(
                child,
                bracket_start_history,
                results,
                counter,
                parent_name
            )

        # ----------------------------------------------------
        # RETURN TO PARENT
        #
        # The bracket is a diversion, so its moves are NOT
        # added to the parent history.
        # ----------------------------------------------------


# ============================================================
# COMPLETE GAMES
# ============================================================

def build_all_complete_games(
    sections,
    variation_map
):

    complete_games = {}

    numbered_cache = {}

    # ========================================================
    # FIRST: BUILD TRUNK + NUMBERED VARIATIONS
    # ========================================================

    for section in sections:

        name = section["name"]

        complete_games[name] = (
            build_numbered_game(
                name,
                variation_map,
                numbered_cache
            )
        )

    # ========================================================
    # SECOND: BUILD BRACKET VARIATIONS
    # ========================================================

    bracket_counter = [
        0
    ]

    for section in sections:

        section_name = section["name"]

        # ----------------------------------------------------
        # IMPORTANT:
        #
        # For T:
        #
        #     base history = []
        #
        # because the T section itself must be walked from
        # the beginning.
        #
        # For Vn:
        #
        #     base history = COMPLETE PARENT GAME
        #
        # NOT the complete Vn game.
        # ----------------------------------------------------

        if section_name == "T":

            base_history = []

        else:

            parent_name = (
                variation_map[
                    section_name
                ]["parent"]
            )

            base_history = (
                complete_games[
                    parent_name
                ]
            )

        bracket_games = (
            extract_all_bracket_games(
                section["text"],
                base_history,
                section_name,
                bracket_counter
            )
        )

        for game in bracket_games:

            complete_games[
                game["name"]
            ] = game["moves"]

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


def write_complete_games(
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
# DISPLAY
# ============================================================

def print_sections(
    sections
):

    print()
    print(
        "=== SECTIONS ==="
    )

    for section in sections:

        moves = get_section_direct_moves(
            section["text"]
        )

        print()
        print(
            section["name"]
        )

        if section["parent"]:

            print(
                f"  declared parent: "
                f"{section['parent']}"
            )

        print(
            f"  direct moves found: "
            f"{len(moves)}"
        )

        print(
            f"  first moves: "
            f"{moves[:8]}"
        )


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
            f"({info['marker']})"
        )

        print(
            f"  replaces: "
            f"{info['branch_move']}"
        )


def print_bracket_trees(
    sections
):

    print()
    print(
        "=== BRACKET TREES BY SECTION ==="
    )

    for section in sections:

        print()
        print(
            f"=== {section['name']} ==="
        )

        tree = parse_bracket_tree(
            section["text"]
        )

        has_bracket = any(
            item_type == "bracket"
            for item_type, value
            in tree["items"]
        )

        if not has_bracket:

            print(
                "NO BRACKETS"
            )

            continue

        print_bracket_tree(
            tree
        )


def print_bracket_tree(
    node,
    depth=0
):

    indent = "    " * depth

    for item_type, value in node["items"]:

        if item_type == "text":

            moves = extract_moves(
                value
            )

            if moves:

                print(
                    f"{indent}MOVES: "
                    f"{moves}"
                )

        else:

            print(
                f"{indent}[ BRACKET OPEN"
            )

            print_bracket_tree(
                value,
                depth + 1
            )

            print(
                f"{indent}] BRACKET CLOSE"
            )


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
            f"{name}: "
            f"{len(moves)} moves"
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
            "python "
            "src/variation_extractor.py "
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
    # SPLIT NUMBERED SECTIONS
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
    # FIND NUMBERED BRANCH POINTS
    # --------------------------------------------------------

    resolve_branch_points(
        variation_map
    )

    # --------------------------------------------------------
    # DISPLAY STRUCTURE
    # --------------------------------------------------------

    print_sections(
        sections
    )

    print_variation_map(
        variation_map
    )

    print_bracket_trees(
        sections
    )

    # --------------------------------------------------------
    # BUILD COMPLETE GAMES
    # --------------------------------------------------------

    complete_games = (
        build_all_complete_games(
            sections,
            variation_map
        )
    )

    # --------------------------------------------------------
    # DISPLAY COMPLETE GAMES
    # --------------------------------------------------------

    print_complete_games(
        complete_games
    )

    # --------------------------------------------------------
    # WRITE FILES
    # --------------------------------------------------------

    output_dir = (
        input_path.parent
        / "output"
    )

    write_complete_games(
        complete_games,
        output_dir
    )

    print()
    print(
        "=== DONE ==="
    )

    print(
        f"Total complete games: "
        f"{len(complete_games)}"
    )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()