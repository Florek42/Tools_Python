import tkinter as tk
from tkinter import messagebox


class SudokuSolverGUI:

  def __init__(self, root):
    self.root = root
    self.root.title("Sudoku Solver By Forek")
    self.root.configure(bg='#2C3E50')
    self.input_frame = tk.Frame(self.root, bg='#2C3E50')
    self.input_frame.pack()

    # 3x3 fields
    self.boxes = [[None for _ in range(3)] for _ in range(3)]
    for i in range(3):
      for j in range(3):
        box_frame = tk.Frame(self.input_frame,
                             borderwidth=2,
                             relief="solid",
                             bg='#34495E')
        box_frame.grid(row=i, column=j, padx=5, pady=5)

        # 3x3 inside
        entries_box = [[None for _ in range(3)] for _ in range(3)]
        for x in range(3):
          for y in range(3):
            entry = tk.Entry(box_frame,
                             width=3,
                             font=('Arial', 12),
                             justify='center')
            entry.grid(row=x, column=y, padx=2, pady=2)
            entry.config(validate="key",
                         validatecommand=(entry.register(self.validate_entry),
                                          '%P'))
            entries_box[x][y] = entry

        self.boxes[i][j] = entries_box

    # solve
    solve_button = tk.Button(self.root,
                             text="Solve",
                             command=self.solve_sudoku,
                             bg='#3498DB',
                             fg='#ECF0F1')
    solve_button.pack(pady=10)

  def validate_entry(self, value):
    # check if int is 1-9
    if value.isdigit():
      if 1 <= int(value) <= 9:
        return True
    elif value == "":
      return True
    return False

  def solve_sudoku(self):
    # main algoritm
    board = [[0 for _ in range(9)] for _ in range(9)]
    for i in range(3):
      for j in range(3):
        for x in range(3):
          for y in range(3):
            value = self.boxes[i][j][x][y].get()
            if value.isdigit():
              board[i * 3 + x][j * 3 + y] = int(value)

    if self.solve(board):
      for i in range(3):
        for j in range(3):
          numbers_in_box = set()
          for x in range(3):
            for y in range(3):
              value = str(board[i * 3 + x][j * 3 + y])
              self.boxes[i][j][x][y].delete(0, tk.END)
              self.boxes[i][j][x][y].insert(0, value)
              if board[i * 3 + x][j * 3 + y] != 0:
                self.boxes[i][j][x][y].config(fg="green")
                numbers_in_box.add(board[i * 3 + x][j * 3 + y])

          # check for repeats
          if len(numbers_in_box) != 9:
            messagebox.showinfo(
                "Info",
                "Numbers can't be the same in one 3x3!")
            return

      messagebox.showinfo("Info", "Sudoku solved successfully!")
    else:
      messagebox.showinfo(
          "Info", "This board can't be solved. Check if numbers are correct!")

  def is_valid(self, board, row, col, num):
    for i in range(9):
      if board[row][i] == num or board[i][col] == num or board[
          row - row % 3 + i // 3][col - col % 3 + i % 3] == num:
        return False
    return True

  def solve(self, board):
    # backtracking
    for i in range(9):
      for j in range(9):
        if board[i][j] == 0:
          for num in range(1, 10):
            if self.is_valid(board, i, j, num):
              board[i][j] = num
              if self.solve(board):
                return True
              board[i][j] = 0  # Backtracking, if can not put number
          return False
    return True


if __name__ == "__main__":
  root = tk.Tk()
  app = SudokuSolverGUI(root)
  root.mainloop()
