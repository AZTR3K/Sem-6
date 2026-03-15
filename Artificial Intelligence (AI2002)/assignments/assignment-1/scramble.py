import json
from main import solve_cube

try:
    print("Loading Pattern Database... (This might take a few seconds)")
    with open("cube_db.json", "r") as f:
        PATTERN_DB = json.load(f)
    print(f"Loaded Pattern Database with {len(PATTERN_DB)} states.\n")
except FileNotFoundError:
    print("Warning: cube_db.json not found. Heuristic will fall back to a weak default.")
    PATTERN_DB = {}


def get_scramble_from_solution(solution_path):
    # 1. Reverse the order of the moves
    reversed_path = solution_path[::-1]

    scramble = []
    # 2. Invert the direction of each move
    for move in reversed_path:
        if "'" in move:
            scramble.append(move[0])      # F' becomes F
        else:
            scramble.append(move + "'")   # F becomes F'

    return " ".join(scramble)


if __name__ == "__main__":
    print("Provide state to get scramble moves. Given that you keep front face green, left orange, bottom yellow.")
    while True:
        state = input("Enter state (n to exit): ").upper().strip()
        if state == "N":
            break

        state = state.replace(" ", "")

        while len(state) != 24:
            state = input("Invalid string, enter again: ")

        path = solve_cube(state)

        exact_scramble = get_scramble_from_solution(path)
        print(f"Scramble sequence to achieve this: {exact_scramble}\n")
