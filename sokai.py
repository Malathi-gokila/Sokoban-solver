import tkinter as tk
import tkinter.messagebox as messagebox
import time
import copy
import collections

# Grid configurations for levels
grid_level1 = [
    list("OOOOOOOO"),
    list("O   OP O"),
    list("O    B O"),
    list("O  O   O"),
    list("OOOOOBGO"),
    list("O G    O"),
    list("OOOOOOOO")
]

grid_level2 = [
    list("OOOOO"),
    list("OGPOO"),
    list("OBBGO"),
    list("O B O"),
    list("O G O"),
    list("OO  O"),
    list(" OOOO")
]

grid_level3=[
    list("OOOOOO"),
    list("OOOPGO"),
    list("OG B O"),
    list("OO B O"),
    list("OGB OO"),
    list(" OOOOO")
]

class SokobanGUI:
    def __init__(self, master, grid):
        self.master = master
        self.grid = grid
        self.initial_grid = [row[:] for row in grid]  # Make a deep copy of the initial grid
        self.player_position = self.find_player_position()
        self.box_positions = self.find_box_positions()
        self.goal_positions = self.find_goal_positions()

        self.canvas = tk.Canvas(master, width=len(grid[0]) * 40, height=len(grid) * 40, bg='lightblue')
        self.canvas.pack(pady=20)

        self.load_images()
        self.draw_grid()

    def load_images(self):
        self.wall_image = tk.PhotoImage(file="C:\\Users\\MALATHI GANESAN\\OneDrive\\Desktop\\wall.png")
        self.player_image = tk.PhotoImage(file="C:\\Users\\MALATHI GANESAN\\OneDrive\\Desktop\\playerD.png")
        self.box_image = tk.PhotoImage(file="C:\\Users\\MALATHI GANESAN\\OneDrive\\Desktop\\box.png")
        self.goal_image = tk.PhotoImage(file="C:\\Users\\MALATHI GANESAN\\OneDrive\\Desktop\\target.png")
        self.box_on_goal_image = tk.PhotoImage(file="C:\\Users\\MALATHI GANESAN\\OneDrive\\Desktop\\valid_box.png")

    def reset_game(self):
        self.grid = [row[:] for row in self.initial_grid]  # Reset grid to its initial state
        self.player_position = self.find_player_position()
        self.box_positions = self.find_box_positions()
        self.goal_positions = self.find_goal_positions()
        self.draw_grid()

    def find_player_position(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.grid[y][x] == 'P':
                    return x, y
        return None

    def find_box_positions(self):
        boxes = []
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.grid[y][x] == 'B':
                    boxes.append((x, y))
        return boxes

    def find_goal_positions(self):
        goals = []
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.grid[y][x] == 'G':
                    goals.append((x, y))
        return goals

    def draw_grid(self):
        self.canvas.delete("all")
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                x0, y0 = x * 40, y * 40
                if cell == 'O':
                    self.canvas.create_image(x0, y0, anchor='nw', image=self.wall_image)
                elif cell == 'P':
                    self.canvas.create_image(x0, y0, anchor='nw', image=self.player_image)
                elif cell == 'B':
                    self.canvas.create_image(x0, y0, anchor='nw', image=self.box_image)
                elif cell == 'G':
                    self.canvas.create_image(x0, y0, anchor='nw', image=self.goal_image)
                elif cell == 'GB':
                    self.canvas.create_image(x0, y0, anchor='nw', image=self.box_on_goal_image)

        # Draw boxes over goal states separately
        for x, y in self.box_positions:
            if self.grid[y][x] == 'GB':
                x0, y0 = x * 40, y * 40
                self.canvas.create_image(x0, y0, anchor='nw', image=self.box_on_goal_image)

    def move_player(self, direction):
        x, y = self.player_position
        dx, dy = direction
        new_x, new_y = x + dx, y + dy

        if self.grid[new_y][new_x] == 'O':
            return False  # Cannot move into walls

        elif self.grid[new_y][new_x] == 'B' or self.grid[new_y][new_x] == 'GB':
            # Check if the box can be pushed
            new_box_x, new_box_y = new_x + dx, new_y + dy
            if self.grid[new_box_y][new_box_x] in ['O', 'B', 'GB']:
                return False  # Cannot push the box into walls or other boxes
            # Move the box
            if self.grid[new_box_y][new_box_x] == 'G':
                self.grid[new_box_y][new_box_x] = 'GB'  # Box placed on goal state
            else:
                self.grid[new_box_y][new_box_x] = 'B'

            if self.grid[new_y][new_x] == 'GB':
                self.grid[new_y][new_x] = 'G'  # Restore goal state
            else:
                self.grid[new_y][new_x] = ' '
            self.box_positions.remove((new_x, new_y))
            self.box_positions.append((new_box_x, new_box_y))

        elif self.grid[new_y][new_x] == 'G':
            # Moving onto a goal state
            pass  # No additional logic needed, just proceed to move player

        elif self.grid[new_y][new_x] == ' ':
            # Moving to an empty space
            pass  # No additional logic needed, just proceed to move player

        # Move the player
        if self.grid[y][x] == 'P':
            if (x, y) in self.goal_positions:
                self.grid[y][x] = 'G'  # Restore goal state
            else:
                self.grid[y][x] = ' '
        elif self.grid[y][x] == 'GP':
            self.grid[y][x] = 'G'  # Restore goal state

        self.grid[new_y][new_x] = 'P'
        self.player_position = (new_x, new_y)

        self.draw_grid()
        self.check_win()
        return True

    def check_win(self):
        for box_x, box_y in self.box_positions:
            if (box_x, box_y) not in self.goal_positions:
                return
        self.display_win_message()

    def display_win_message(self):
        messagebox.showinfo("Congratulations!", "You Win!")
        self.master.destroy()
        choose_level()

    def follow_path(self, path):
        for move in path:
            direction = {
                'U': (0, -1),
                'D': (0, 1),
                'L': (-1, 0),
                'R': (1, 0)
            }[move]
            self.move_player(direction)
            self.master.update()
            time.sleep(0.5)  # Adjust speed of automatic movement

def solve_sokoban(grid):
    maxRowLength = len(grid[0])
    lines = len(grid)

    boxRobot = []
    wallsStorageSpaces = []
    possibleMoves = {'U': [-1, 0], 'R': [0, 1], 'D': [1, 0], 'L': [0, -1]}

    for i in range(lines):
        boxRobot.append(['-'] * maxRowLength)
        wallsStorageSpaces.append(['-'] * maxRowLength)

    for i in range(len(grid)):
        for j in range(maxRowLength):
            if grid[i][j] == 'B' or grid[i][j] == 'P':
                boxRobot[i][j] = grid[i][j]
                wallsStorageSpaces[i][j] = ' '
            elif grid[i][j] == 'G' or grid[i][j] == 'O':
                wallsStorageSpaces[i][j] = grid[i][j]
                boxRobot[i][j] = ' '
            elif grid[i][j] == ' ':
                boxRobot[i][j] = ' '
                wallsStorageSpaces[i][j] = ' '
            elif grid[i][j] == '*':
                boxRobot[i][j] = 'B'
                wallsStorageSpaces[i][j] = 'G'
            elif grid[i][j] == '.':
                boxRobot[i][j] = 'P'
                wallsStorageSpaces[i][j] = 'G'

    movesList = []
    visitedMoves = []

    queue = collections.deque([])
    source = [boxRobot, movesList]
    if boxRobot not in visitedMoves:
        visitedMoves.append(boxRobot)
    queue.append(source)
    robot_x = -1
    robot_y = -1
    completed = 0
    solution_path = []

    while len(queue) != 0 and completed == 0:
        temp = queue.popleft()
        curPosition = temp[0]
        movesTillNow = temp[1]
        for i in range(lines):
            for j in range(maxRowLength):
                if curPosition[i][j] == 'P':
                    robot_y = j
                    robot_x = i
                    break
            else:
                continue
            break

        for key in possibleMoves:
            robotNew_x = robot_x + possibleMoves[key][0]
            robotNew_y = robot_y + possibleMoves[key][1]
            curPositionCopy = copy.deepcopy(curPosition)
            movesTillNowCopy = copy.deepcopy(movesTillNow)
            if curPositionCopy[robotNew_x][robotNew_y] == 'B':
                boxNew_x = robotNew_x + possibleMoves[key][0]
                boxNew_y = robotNew_y + possibleMoves[key][1]
                if curPositionCopy[boxNew_x][boxNew_y] == 'B' or wallsStorageSpaces[boxNew_x][boxNew_y] == 'O':
                    continue
                else:
                    curPositionCopy[boxNew_x][boxNew_y] = 'B'
                    curPositionCopy[robotNew_x][robotNew_y] = 'P'
                    curPositionCopy[robot_x][robot_y] = ' '
                    if curPositionCopy not in visitedMoves:
                        matches = 0
                        for k in range(lines):
                            for l in range(maxRowLength):
                                if wallsStorageSpaces[k][l] == 'G':
                                    if curPositionCopy[k][l] != 'B':
                                        matches = 1
                        movesTillNowCopy.append(key)
                        if matches == 0:
                            completed = 1
                            solution_path = movesTillNowCopy
                            break
                        else:
                            queue.appendleft([curPositionCopy, movesTillNowCopy])
                            visitedMoves.append(curPositionCopy)
            else:
                if wallsStorageSpaces[robotNew_x][robotNew_y] == 'O' or curPositionCopy[robotNew_x][robotNew_y] != ' ':
                    continue
                else:
                    curPositionCopy[robotNew_x][robotNew_y] = 'P'
                    curPositionCopy[robot_x][robot_y] = ' '

                    if curPositionCopy not in visitedMoves:
                        movesTillNowCopy.append(key)
                        queue.appendleft([curPositionCopy, movesTillNowCopy])
                        visitedMoves.append(curPositionCopy)

    if completed == 0:
        print("Can't make it")
    return solution_path

def choose_level():
    selection_window = tk.Tk()
    selection_window.title("Choose Level")

    label = tk.Label(selection_window, text="Choose a level to start", font=("Helvetica", 16, "bold"), bg='lightblue')
    label.pack(pady=20)

    button_level1 = tk.Button(selection_window, text="Level 1", command=lambda: [selection_window.destroy(), start_level(1)],
                              font=("Helvetica", 14), bg='lightgreen', activebackground='darkgreen')
    button_level1.pack(pady=10)

    button_level2 = tk.Button(selection_window, text="Level 2", command=lambda: [selection_window.destroy(), start_level(2)],
                              font=("Helvetica", 14), bg='lightgreen', activebackground='darkgreen')
    button_level2.pack(pady=10)

    button_level3 = tk.Button(selection_window, text="Level 3", command=lambda: [selection_window.destroy(), start_level(3)],
                              font=("Helvetica", 14), bg='lightgreen', activebackground='darkgreen')
    button_level3.pack(pady=10)

    button_close = tk.Button(selection_window, text="Close", command=selection_window.destroy,
                             font=("Helvetica", 14), bg='lightcoral', activebackground='darkred')
    button_close.pack(pady=10)

    selection_window.configure(bg='lightblue')
    selection_window.mainloop()

def start_level(level):
    global current_level  # Declare current_level as global so it can be modified inside the function
    current_level = level  # Set the current level to the selected level

    def solve_and_play():
        nonlocal sokoban_gui, grid
        sokoban_gui.reset_game()  # Reset the game state before starting a new level
        solution_path = solve_sokoban(grid)
        if solution_path:
            print("Solution path:", ''.join(solution_path))
            sokoban_gui.follow_path(solution_path)
        else:
            print("No solution found.")

    root = tk.Tk()
    root.title(f"Sokoban - Level {level}")

    if level == 1:
        grid = grid_level1
    elif level == 2:
        grid = grid_level2
    elif level == 3:
        grid = grid_level3

    sokoban_gui = SokobanGUI(root, grid)

    start_button = tk.Button(root, text="Start", command=solve_and_play, font=("Helvetica", 14), bg='lightgreen', activebackground='darkgreen')
    start_button.pack(pady=20)

    root.configure(bg='lightblue')
    root.mainloop()

current_level = 1  # Initialize the current level to 1

choose_level()
