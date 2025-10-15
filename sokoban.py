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

grid_level3 = [
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
        self.initial_grid = [row[:] for row in grid]
        self.player_position = self.find_player_position()
        self.box_positions = self.find_box_positions()
        self.goal_positions = self.find_goal_positions()

        self.canvas = tk.Canvas(master, width=len(grid[0]) * 40, height=len(grid) * 40, bg='lightblue')
        self.canvas.pack(pady=20)

        self.load_images()
        self.draw_grid()

    def load_images(self):
        self.wall_image = tk.PhotoImage(file="D:\\placement\\PROJ\\projects\\ai proj\\ai proj\\wall.png")
        self.player_image = tk.PhotoImage(file="D:\\placement\\PROJ\\projects\\ai proj\\ai proj\\playerD.png")
        self.box_image = tk.PhotoImage(file="D:\\placement\\PROJ\\projects\\ai proj\\ai proj\\box.png")
        self.goal_image = tk.PhotoImage(file="D:\\placement\\PROJ\\projects\\ai proj\\ai proj\\target.png")
        self.box_on_goal_image = tk.PhotoImage(file="D:\\placement\\PROJ\\projects\\ai proj\\ai proj\\valid_box.png")

    def reset_game(self):
        self.grid = [row[:] for row in self.initial_grid]
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

    def move_player(self, direction):
        x, y = self.player_position
        dx, dy = direction
        new_x, new_y = x + dx, y + dy

        if self.grid[new_y][new_x] == 'O':
            return False

        elif self.grid[new_y][new_x] in ['B', 'GB']:
            new_box_x, new_box_y = new_x + dx, new_y + dy
            if self.grid[new_box_y][new_box_x] in ['O', 'B', 'GB']:
                return False

            if self.grid[new_box_y][new_box_x] == 'G':
                self.grid[new_box_y][new_box_x] = 'GB'
            else:
                self.grid[new_box_y][new_box_x] = 'B'

            if self.grid[new_y][new_x] == 'GB':
                self.grid[new_y][new_x] = 'G'
            else:
                self.grid[new_y][new_x] = ' '

            self.box_positions.remove((new_x, new_y))
            self.box_positions.append((new_box_x, new_box_y))

        self.grid[y][x] = 'G' if (x, y) in self.goal_positions else ' '
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
        # Safer: only show message if window still exists
        if not self.master.winfo_exists():
            return
        try:
            messagebox.showinfo("Congratulations!", "You Win!")
            self.master.destroy()
            choose_level()
        except tk.TclError:
            pass

    def follow_path(self, path):
        for move in path:
            if not self.master.winfo_exists():
                return
            try:
                direction = {'U': (0, -1), 'D': (0, 1), 'L': (-1, 0), 'R': (1, 0)}[move]
                self.move_player(direction)
                if self.master.winfo_exists():
                    self.master.update()
                time.sleep(0.5)
            except tk.TclError:
                return

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
            if grid[i][j] in ['B', 'P']:
                boxRobot[i][j] = grid[i][j]
                wallsStorageSpaces[i][j] = ' '
            elif grid[i][j] in ['G', 'O']:
                wallsStorageSpaces[i][j] = grid[i][j]
                boxRobot[i][j] = ' '
            elif grid[i][j] == ' ':
                boxRobot[i][j] = ' '
                wallsStorageSpaces[i][j] = ' '

    movesList = []
    visitedMoves = []
    queue = collections.deque([])
    source = [boxRobot, movesList]
    visitedMoves.append(boxRobot)
    queue.append(source)
    solution_path = []
    completed = 0

    while queue and not completed:
        temp = queue.popleft()
        curPosition = temp[0]
        movesTillNow = temp[1]
        robot_x, robot_y = -1, -1

        for i in range(lines):
            for j in range(maxRowLength):
                if curPosition[i][j] == 'P':
                    robot_x, robot_y = i, j
                    break
            if robot_x != -1:
                break

        for key, (dx, dy) in possibleMoves.items():
            robotNew_x, robotNew_y = robot_x + dx, robot_y + dy
            curCopy = copy.deepcopy(curPosition)
            movesCopy = copy.deepcopy(movesTillNow)

            if curCopy[robotNew_x][robotNew_y] == 'B':
                boxNew_x, boxNew_y = robotNew_x + dx, robotNew_y + dy
                if curCopy[boxNew_x][boxNew_y] == 'B' or wallsStorageSpaces[boxNew_x][boxNew_y] == 'O':
                    continue
                curCopy[boxNew_x][boxNew_y] = 'B'
                curCopy[robotNew_x][robotNew_y] = 'P'
                curCopy[robot_x][robot_y] = ' '
            elif wallsStorageSpaces[robotNew_x][robotNew_y] != 'O' and curCopy[robotNew_x][robotNew_y] == ' ':
                curCopy[robotNew_x][robotNew_y] = 'P'
                curCopy[robot_x][robot_y] = ' '
            else:
                continue

            if curCopy not in visitedMoves:
                movesCopy.append(key)
                visitedMoves.append(curCopy)
                queue.appendleft([curCopy, movesCopy])
                if all(curCopy[i][j] == 'B' if wallsStorageSpaces[i][j] == 'G' else True
                       for i in range(lines) for j in range(maxRowLength)):
                    solution_path = movesCopy
                    completed = 1
                    break

    return solution_path

def choose_level():
    selection_window = tk.Tk()
    selection_window.title("Choose Level")

    label = tk.Label(selection_window, text="Choose a level to start",
                     font=("Helvetica", 16, "bold"), bg='lightblue')
    label.pack(pady=20)

    for level in [1, 2, 3]:
        tk.Button(
            selection_window, text=f"Level {level}",
            command=lambda l=level: [selection_window.destroy(), start_level(l)],
            font=("Helvetica", 14), bg='lightgreen', activebackground='darkgreen'
        ).pack(pady=10)

    tk.Button(selection_window, text="Close", command=selection_window.destroy,
              font=("Helvetica", 14), bg='lightcoral', activebackground='darkred').pack(pady=10)

    selection_window.configure(bg='lightblue')
    selection_window.mainloop()

def start_level(level):
    def on_close():
        try:
            root.destroy()
        except:
            pass

    def solve_and_play():
        nonlocal sokoban_gui, grid
        try:
            sokoban_gui.reset_game()
            solution_path = solve_sokoban(grid)
            if solution_path:
                print("Solution path:", ''.join(solution_path))
                sokoban_gui.follow_path(solution_path)
            else:
                print("No solution found.")
        except tk.TclError:
            pass

    root = tk.Tk()
    root.title(f"Sokoban - Level {level}")
    root.protocol("WM_DELETE_WINDOW", on_close)
    grid = [grid_level1, grid_level2, grid_level3][level - 1]

    sokoban_gui = SokobanGUI(root, grid)
    tk.Button(root, text="Start", command=solve_and_play,
              font=("Helvetica", 14), bg='lightgreen', activebackground='darkgreen').pack(pady=20)

    root.configure(bg='lightblue')
    root.mainloop()

# Start the game
choose_level()
