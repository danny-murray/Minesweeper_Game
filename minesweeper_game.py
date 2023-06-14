''' Minesweeper - the Game '''

# Importing modules
import tkinter as tk
from tkinter import messagebox
import random
import time
import threading

# GUI setup
class MinesweeperGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Minesweeper")
        self.rows = 0
        self.columns = 0
        self.mine_count = 0
        self.grid = []
        self.buttons = []
        self.started = False
        self.game_over = False
        self.remaining_cells = 0
        self.timer = None
        self.time_elapsed = 0
        self.create_menu()

    # Difficulty Level Menu Bar
    def create_menu(self):
        menu_bar = tk.Menu(self.master)
        difficulty_menu = tk.Menu(menu_bar, tearoff=0)
        difficulty_menu.add_command(label="Easy", command=lambda: self.start_game(8, 8, 10))
        difficulty_menu.add_command(label="Difficult", command=lambda: self.start_game(12, 12, 20))
        difficulty_menu.add_command(label="Expert", command=lambda: self.start_game(16, 16, 40))
        menu_bar.add_cascade(label="Choose your difficulty level:", menu=difficulty_menu)
        self.master.config(menu=menu_bar)

    # New Game function
    def start_game(self, rows, columns, mine_count):
        # Game parameters
        self.rows = rows
        self.columns = columns
        self.mine_count = mine_count
        # Game grid
        self.grid = [[' ' for _ in range(columns)] for _ in range(rows)]
        # Game variables
        self.buttons = []
        self.started = False
        self.game_over = False
        self.remaining_cells = rows * columns - mine_count
        # Game timer setup
        self.timer_label = tk.Label(self.master, text="Time: 0")
        self.timer_label.pack()
        # Grid buttons and time starter
        self.create_grid_buttons()
        self.start_timer()

    # Grid buttons function
    def create_grid_buttons(self):
        # Create the grid buttons
        self.button_frame = tk.Frame(self.master)
        self.button_frame.pack()

        # Iterating through rows and columns to create buttons
        for row in range(self.rows):
            button_row = []
            for col in range(self.columns):
                # Button widget
                button = tk.Button(self.button_frame, width=2, relief=tk.RAISED)
                button.grid(row=row, column=col)    # button position
                button.bind('<Button-1>', lambda e, r=row, c=col: self.left_click(r, c))
                button_row.append(button)   # adding button to row
            self.buttons.append(button_row) # adding to button list

    # User Left Click function
    def left_click(self, row, col):
        # Checks if game has started, if not places mines on grid
        if not self.started:
            self.place_mines(row, col)
            self.started = True
            
        # Checks if the clicked cell contains a mine
        if self.grid[row][col] == 'X':
            # Reveal entire grid if user hits a mine, end game
            self.reveal_grid()
            self.game_over = True
            messagebox.showinfo("Game Over!", "You've hit a mine! Game over.")
        else:
            # If cell is cLear, reveal the cell
            self.reveal_cell(row, col)
            # Check if all clear cells are revealed. If so, end game, user wins
            if self.remaining_cells == 0:
                self.game_over = True
                messagebox.showinfo("Congratulations!", "You've won!")

    # Function for randomised mine placing
    def place_mines(self, row, col):
        mines = 0
        # While Loop until number of mines placed
        while mines < self.mine_count:
            # Randomised coordinates
            rand_row = random.randint(0, self.rows - 1)
            rand_col = random.randint(0, self.columns - 1)
            # Check to see if selected cell already contains a mine
            if self.grid[rand_row][rand_col] != 'X' and (rand_row != row or rand_col != col):
                # Place mine at selected cell
                self.grid[rand_row][rand_col] = 'X'
                mines += 1

    # Updating buttons, revealing grid
    def reveal_grid(self):
        # Iterating over grid
        for row in range(self.rows):
            for col in range(self.columns):
                # If cell contains mine ('X'), update button colour and text
                if self.grid[row][col] == 'X':
                    self.buttons[row][col].config(text='X', bg='red')
                # Otherwise disable button
                else:
                    self.buttons[row][col].config(text=self.grid[row][col], state=tk.DISABLED)

    # Revealing cells and updating counts
    def reveal_cell(self, row, col):
        if self.grid[row][col] == ' ':
            self.remaining_cells -= 1
            neighbours = self.get_neighbour_indices(row, col)
            mine_count = 0
            for neighbour in neighbours:
                n_row, n_col = neighbour
                if self.grid[n_row][n_col] == 'X':
                    mine_count += 1
            self.grid[row][col] = str(mine_count)
            self.buttons[row][col].config(text=str(mine_count), state=tk.DISABLED)
            if mine_count == 0:
                for neighbour in neighbours:
                    n_row, n_col = neighbour
                    if self.grid[n_row][n_col] == ' ':
                        self.reveal_cell(n_row, n_col)
        elif self.grid[row][col].isdigit():
            self.remaining_cells -= 1
            self.buttons[row][col].config(text=self.grid[row][col], state=tk.DISABLED)

    # Reveals neighbouring cell indices for given row and column
    def get_neighbour_indices(self, row, col):
        indices = []
        for r in range(max(0, row - 1), min(self.rows, row + 2)):
            for c in range(max(0, col - 1), min(self.columns, col + 2)):
                if r != row or c != col:
                    indices.append((r, c))
        return indices

    # Initiates game timer
    def start_timer(self):
        self.timer = threading.Timer(1, self.update_timer) # calls update_time every 1 second
        self.timer.start()

    # Updating timer with 1 second increments
    def update_timer(self):
        self.time_elapsed += 1
        self.timer_label.config(text="Time: " + str(self.time_elapsed))
        self.start_timer()

# Creating Tkinter window
root = tk.Tk()

# Creating Minesweeper GUI
minesweeper = MinesweeperGUI(root
                             )
# Starts Tkinter event loop
root.mainloop()
