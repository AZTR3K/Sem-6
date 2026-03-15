import json
from collections import deque
from RubiksCube2x2x2 import Cube


def generate_pattern_database(max_depth):
    all_goals = [
        # White on Top
        "WWWW RRRR GGGG YYYY OOOO BBBB",
        "WWWW BBBB RRRR YYYY GGGG OOOO",
        "WWWW OOOO BBBB YYYY RRRR GGGG",
        "WWWW GGGG OOOO YYYY BBBB RRRR",

        # Yellow on Top
        "YYYY OOOO GGGG WWWW RRRR BBBB",
        "YYYY GGGG RRRR WWWW BBBB OOOO",
        "YYYY RRRR BBBB WWWW OOOO GGGG",
        "YYYY BBBB OOOO WWWW GGGG RRRR",

        # Green on Top
        "GGGG RRRR YYYY BBBB OOOO WWWW",
        "GGGG WWWW RRRR BBBB YYYY OOOO",
        "GGGG OOOO WWWW BBBB RRRR YYYY",
        "GGGG YYYY OOOO BBBB WWWW RRRR",

        # Blue on Top
        "BBBB RRRR WWWW GGGG OOOO YYYY",
        "BBBB YYYY RRRR GGGG WWWW OOOO",
        "BBBB OOOO YYYY GGGG RRRR WWWW",
        "BBBB WWWW OOOO GGGG YYYY RRRR",

        # Red on Top
        "RRRR WWWW GGGG OOOO YYYY BBBB",
        "RRRR BBBB WWWW OOOO GGGG YYYY",
        "RRRR YYYY BBBB OOOO WWWW GGGG",
        "RRRR GGGG YYYY OOOO BBBB WWWW",

        # Orange on Top
        "OOOO YYYY GGGG RRRR WWWW BBBB",
        "OOOO BBBB YYYY RRRR GGGG WWWW",
        "OOOO WWWW BBBB RRRR YYYY GGGG",
        "OOOO GGGG WWWW RRRR BBBB YYYY"
    ]

    clean_goals = [goal.replace(" ", "") for goal in all_goals]

    queue = deque([(goal, 0) for goal in clean_goals])
    pattern_db = {goal: 0 for goal in clean_goals}
    moves = ["F", "F'", "U", "U'", "R", "R'", "L", "L'", "B", "B'", "D", "D'"]
    nodes_generated = 0

    print(f"Generating Pattern Database up to depth {max_depth} from all 24 goals...")

    while len(queue) != 0:
        current_state, depth = queue.popleft()

        if depth == max_depth:
            continue

        for move in moves:
            cube = Cube(current_state).make_move(move)
            if cube.state not in pattern_db:
                new_depth = depth + 1
                pattern_db[cube.state] = new_depth
                nodes_generated += 1
                queue.append((cube.state, new_depth))

    print(f"Finished! Database contains {len(pattern_db)} states.")

    with open("cube_db.json", "w") as f:
        json.dump(pattern_db, f)
    print("Saved to cube_db.json")


if __name__ == "__main__":
    generate_pattern_database(max_depth=10)
