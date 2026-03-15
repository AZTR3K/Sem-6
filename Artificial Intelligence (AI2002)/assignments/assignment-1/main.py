# Rollno: 23L - 0515
# Section: 6C
import time
import json
import heapq as hq

# Load Database
s = time.time()
try:
    print("Loading Pattern Database...")
    with open("cube_db.json", "r") as f:
        PATTERN_DB = json.load(f)
    print(f"Loaded Pattern Database with {len(PATTERN_DB)} states.")
except FileNotFoundError:
    print("Warning: cube_db.json not found. Heuristic will fall back to a weak default.")
    PATTERN_DB = {}
e = time.time()
print(f"Time taken: {e - s}\n")


class Cube:
    def __init__(self, str):
        self.state = str.replace(" ", "")

        if len(self.state) != 24:
            raise ValueError(f"Invalid input string: expected 24 color characters, but got {len(self.state)}.")

        self.matrix = self.generate_matrix()

    def generate_matrix(self):
        s = self.state

        matrix = [
            [" ", " ", s[0], s[1], " ", " ", " ", " "],
            [" ", " ", s[2], s[3], " ", " ", " ", " "],
            [s[16], s[17], s[8], s[9], s[4], s[5], s[20], s[21]],
            [s[18], s[19], s[10], s[11], s[6], s[7], s[22], s[23]],
            [" ", " ", s[12], s[13], " ", " ", " ", " "],
            [" ", " ", s[14], s[15], " ", " ", " ", " "]
        ]

        return matrix

    def make_move(self, move):
        match move:
            case "F":
                return self.make_move_f(True)
            case "F'":
                return self.make_move_f(False)
            case "U":
                return self.make_move_u(True)
            case "U'":
                return self.make_move_u(False)
            case "R":
                return self.make_move_r(True)
            case "R'":
                return self.make_move_r(False)
            case "L":
                return self.make_move_l(True)
            case "L'":
                return self.make_move_l(False)
            case "B":
                return self.make_move_b(True)
            case "B'":
                return self.make_move_b(False)
            case "D":
                return self.make_move_d(True)
            case "D'":
                return self.make_move_d(False)

    def make_move_f(self, isClockwise):
        if isClockwise:
            p = [0, 1, 19, 17, 2, 5, 3, 7, 10, 8, 11, 9, 6, 4, 14, 15, 16, 12, 18, 13, 20, 21, 22, 23]
        else:
            p = [0, 1, 4, 6, 13, 5, 12, 7, 9, 11, 8, 10, 17, 19, 14, 15, 16, 3, 18, 2, 20, 21, 22, 23]
        return Cube("".join(self.state[i] for i in p))

    def make_move_u(self, isClockwise):
        if isClockwise:
            p = [2, 0, 3, 1, 20, 21, 6, 7, 4, 5, 10, 11, 12, 13, 14, 15, 8, 9, 18, 19, 16, 17, 22, 23]
        else:
            p = [1, 3, 0, 2, 8, 9, 6, 7, 16, 17, 10, 11, 12, 13, 14, 15, 20, 21, 18, 19, 4, 5, 22, 23]
        return Cube("".join([self.state[i] for i in p]))

    def make_move_r(self, isClockwise):
        if isClockwise:
            p = [0, 9, 2, 11, 6, 4, 7, 5, 8, 13, 10, 15, 12, 22, 14, 20, 16, 17, 18, 19, 3, 21, 1, 23]
        else:
            p = [0, 22, 2, 20, 5, 7, 4, 6, 8, 1, 10, 3, 12, 9, 14, 11, 16, 17, 18, 19, 15, 21, 13, 23]
        return Cube("".join([self.state[i] for i in p]))

    def make_move_l(self, isClockwise):
        if isClockwise:
            p = [23, 1, 21, 3, 4, 5, 6, 7, 0, 9, 2, 11, 8, 13, 10, 15, 18, 16, 19, 17, 20, 14, 22, 12]
        else:
            p = [8, 1, 10, 3, 4, 5, 6, 7, 12, 9, 14, 11, 23, 13, 21, 15, 17, 19, 16, 18, 20, 2, 22, 0]
        return Cube("".join([self.state[i] for i in p]))

    def make_move_b(self, isClockwise):
        if isClockwise:
            p = [18, 16, 2, 3, 4, 0, 6, 1, 8, 9, 10, 11, 12, 13, 7, 5, 14, 17, 15, 19, 21, 23, 20, 22]
        else:
            p = [5, 7, 2, 3, 4, 15, 6, 14, 8, 9, 10, 11, 12, 13, 16, 18, 1, 17, 0, 19, 22, 20, 23, 21]
        return Cube("".join([self.state[i] for i in p]))

    def make_move_d(self, isClockwise):
        if isClockwise:
            p = [0, 1, 2, 3, 4, 5, 10, 11, 8, 9, 18, 19, 14, 12, 15, 13, 16, 17, 22, 23, 20, 21, 6, 7]
        else:
            p = [0, 1, 2, 3, 4, 5, 22, 23, 8, 9, 6, 7, 13, 15, 12, 14, 16, 17, 10, 11, 20, 21, 18, 19]
        return Cube("".join([self.state[i] for i in p]))

    def is_goal_state(self):
        for i in range(0, 24, 4):
            face = self.state[i:i + 4]
            if len(set(face)) != 1:
                return False
        return True

    # Old heuristic
    # def calculate_heuristic(self):
    #    h = 0
    #    for i in range(0, 24, 4):
    #        face = self.state[i:i + 4]
    #        h += len(set(face)) - 1

    #    # Divide by 8 (the max possible change in one move) to guarantee admissibility
    #    return (h + 7) // 8

    def calculate_heuristic(self):
        if self.state in PATTERN_DB:
            return PATTERN_DB[self.state]

        # My database is depth 10, so if a state is not in the dictionary, it is at minimum 11 moves away
        return 11

    def display(self):
        for row in self.matrix:
            print("".join(row))


def solve_cube(input_str):
    try:
        start_cube = Cube(input_str)
        pq = []
        tie_breaker_id = 0

        # Priority queue structure: (f_score, tie_breaker, g_score, state_string, path_list)
        hq.heappush(pq, (start_cube.calculate_heuristic(), tie_breaker_id, 0, start_cube.state, []))

        visited = set()
        visited.add(start_cube.state)

        nodes_generated = 1
        nodes_expanded = 0
        start_time = time.time()

        while len(pq) != 0:
            f, _, g, current_state, path = hq.heappop(pq)
            current_cube = Cube(current_state)

            if current_cube.is_goal_state():
                end_time = time.time()
                print(f"Solution Path: {' '.join(path) if path else 'Already Solved'}")
                print(f"Nodes Generated: {nodes_generated}")
                print(f"Nodes Expanded: {nodes_expanded}")
                print(f"Time Taken: {end_time - start_time:.4f} seconds")
                return current_cube

            nodes_expanded += 1
            moves = ["F", "F'", "U", "U'", "R", "R'", "L", "L'", "B", "B'", "D", "D'"]

            for move in moves:
                new_cube = current_cube.make_move(move)
                if new_cube.state not in visited:
                    visited.add(new_cube.state)
                    nodes_generated += 1

                    new_g = g + 1
                    new_h = new_cube.calculate_heuristic()
                    new_f = new_g + new_h
                    new_path = path + [move]

                    tie_breaker_id += 1
                    hq.heappush(pq, (new_f, tie_breaker_id, new_g, new_cube.state, new_path))

        print("No solution found.")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    print("Testing Hard coded scrambles:")
    tests = {
        "WWWW BBRR RRGG YYYY GGOO OOBB": (1, "U"),
        "WRWG RBRB RYGY YBYO GGOO WOWB": (2, "U R"),
        "WWGR WORB RBGY YBYO RYOO GGWB": (3, "U R U"),
        "WBGY RWBO RBGO YWYG RYOO RGWB": (4, "U R U R"),
        "GWYB RGBO RWGO YWYG RBOO RYWB": (5, "U R U R U"),
        "RGOG RWRB GYWY RBYO WYOG OBWB": (6, "U R U' R' F R"),
        "ORRB RYRB GWWG GYYO GWOO BYWB": (7, "R' U R U' F U F'"),
        "OWYW BOYR GRWG ROYY BROG GWBB": (8, "R U R' U R U R' F'"),
        "ORBR YWRB RGGY YBYO WWOO GGWB": (9, "R U' R' U F' U F R U'"),
        "YWYW BGOR ORBG WWYY GGOO RRBB": (10, "R F' R U R' U' U' R' U' F'"),
        "WWYY OROR GGBG WWYY RROO BGBB": (11, "R F' R U R' U' U' R' U' F' U"),
        "WWOO WRWR GGGB ROYY RYOY BGBB": (12, "R F' R U R' U' U' R' U' F' U F"),
        "WWWW ORRR GBGG YYYY ROOO BGBB": (13, "R F' R U R' U' U' R' U' F' U F F"),
        "WWWW BGRR ORGG YYYY GBOO ROBB": (14, "R F' R U R' U' U' R' U' F' U F F U")
    }

    print("Moves provided for scramble are for user testing. Not given to A* algorithm")
    for test, moves in tests.items():
        depth, scramble = moves
        print(f"Scramble: {test}. Depth: {depth}.")
        print(f"Moves to scramble: {scramble}")
        cube = solve_cube(test)
        formatted_state = " ".join(cube.state[i:i + 4] for i in range(0, 24, 4))
        print(f"Resulting state: {formatted_state}\n")

    print("\nUser Input Testing:")
    choice = input("Do you want to enter custom tests (y/n): ").lower().strip()
    while choice == "y":
        test = input("Enter state: ").upper().strip()
        cube = solve_cube(test)
        if cube:
            formatted_state = " ".join(cube.state[i:i + 4] for i in range(0, 24, 4))
            print(f"Resulting state: {formatted_state}\n")

        choice = input("Continue (y/n): ").lower().strip()
