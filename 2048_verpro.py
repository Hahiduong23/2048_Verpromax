import tkinter as tk
import random
from tkinter import messagebox

# Lớp Tile đại diện cho từng ô trên bảng
class Tile:
    def __init__(self, value=0):
        self.__value = value  # Private attribute

    def set_value(self, value):
        self.__value = value

    def get_value(self):
        return self.__value

# Lớp Board xử lý các thao tác trên bảng 2048
class Board:
    def __init__(self):
        self.__grid = [[Tile() for _ in range(4)] for _ in range(4)]  # Private grid
        self.add_new_tile()
        self.add_new_tile()

    def add_new_tile(self):
        empty_cells = [(i, j) for i in range(4) for j in range(4) if self.__grid[i][j].get_value() == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.__grid[i][j].set_value(2)

    def get_grid_values(self):
        return [[self.__grid[i][j].get_value() for j in range(4)] for i in range(4)]

    def compress(self):
        changed = False
        new_grid = [[Tile() for _ in range(4)] for _ in range(4)]
        for i in range(4):
            pos = 0
            for j in range(4):
                if self.__grid[i][j].get_value() != 0:
                    new_grid[i][pos].set_value(self.__grid[i][j].get_value())
                    if j != pos:
                        changed = True
                    pos += 1
        self.__grid = new_grid
        return changed

    def merge(self):
        changed = False
        for i in range(4):
            for j in range(3):
                if self.__grid[i][j].get_value() == self.__grid[i][j + 1].get_value() and self.__grid[i][j].get_value() != 0:
                    self.__grid[i][j].set_value(self.__grid[i][j].get_value() * 2)
                    self.__grid[i][j + 1].set_value(0)
                    changed = True
        return changed

    def reverse(self):
        for i in range(4):
            self.__grid[i] = self.__grid[i][::-1]

    def transpose(self):
        self.__grid = [list(row) for row in zip(*self.__grid)]

    def move_left(self):
        changed1 = self.compress()
        changed2 = self.merge()
        self.compress()
        return changed1 or changed2

    def move_right(self):
        self.reverse()
        changed = self.move_left()
        self.reverse()
        return changed

    def move_up(self):
        self.transpose()
        changed = self.move_left()
        self.transpose()
        return changed

    def move_down(self):
        self.transpose()
        changed = self.move_right()
        self.transpose()
        return changed

    def check_state(self):
        for i in range(4):
            for j in range(4):
                if self.__grid[i][j].get_value() == 2048:
                    return 'WON'
        for i in range(4):
            for j in range(4):
                if self.__grid[i][j].get_value() == 0:
                    return 'GAME NOT OVER'
        for i in range(3):
            for j in range(3):
                if self.__grid[i][j].get_value() == self.__grid[i + 1][j].get_value() or self.__grid[i][j].get_value() == self.__grid[i][j + 1].get_value():
                    return 'GAME NOT OVER'
        for j in range(3):
            if self.__grid[3][j].get_value() == self.__grid[3][j + 1].get_value():
                return 'GAME NOT OVER'
        for i in range(3):
            if self.__grid[i][3].get_value() == self.__grid[i + 1][3].get_value():
                return 'GAME NOT OVER'
        return 'LOST'

# Lớp Game2048 quản lý giao diện và luồng trò chơi
class Game2048:
    def __init__(self, root):
        self._root = root  # Protected attribute
        self._root.title("2048")
        self._root.geometry("400x400")
        self._board = Board()
        self.create_widgets()
        self.update_grid_ui()

    def create_widgets(self):
        self._frame = tk.Frame(self._root, bg="#bbada0")
        self._frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self._tiles = [[tk.Label(self._frame, text="", width=4, height=2, bg="#cdc1b4", font=('Arial', 24, 'bold'), anchor='center') for _ in range(4)] for _ in range(4)]
        for i in range(4):
            for j in range(4):
                self._tiles[i][j].grid(row=i, column=j, padx=5, pady=5, sticky='nsew')
        for i in range(4):
            self._frame.grid_columnconfigure(i, weight=1)
            self._frame.grid_rowconfigure(i, weight=1)
        self._root.bind("<Key>", self.key_pressed)

    def update_grid_ui(self):
        grid_values = self._board.get_grid_values()
        for i in range(4):
            for j in range(4):
                value = grid_values[i][j]
                color = self.get_color(value)
                text = str(value) if value != 0 else ''
                self._tiles[i][j].config(text=text, bg=color)

    def get_color(self, value):
        colors = {
            2: '#fdd0dc', 4: '#fcb3c2', 8: '#f8a2b7',
            16: '#f7819f', 32: '#f76c7c', 64: '#f64d65',
            128: '#f64d6f', 256: '#f65f6f', 512: '#f67272',
            1024: '#f67d7d', 2048: '#f68888'
        }
        return colors.get(value, '#faf8ef')

    def key_pressed(self, event):
        if event.keysym == 'Up':
            changed = self._board.move_up()
        elif event.keysym == 'Down':
            changed = self._board.move_down()
        elif event.keysym == 'Left':
            changed = self._board.move_left()
        elif event.keysym == 'Right':
            changed = self._board.move_right()
        else:
            return
        if changed:
            self._board.add_new_tile()
        self.update_grid_ui()
        state = self._board.check_state()
        if state == 'WON':
            messagebox.showinfo("2048", "Chúc mừng! Bạn đã thắng!")
            self._root.quit()
        elif state == 'LOST':
            messagebox.showinfo("2048", "Game Over! Bạn đã thua!")
            self._root.quit()

# Lớp Game2048HardMode kế thừa từ Game2048, ghi đè phương thức add_new_tile
class Game2048HardMode(Game2048):
    def __init__(self, root):
        super().__init__(root)  # Gọi phương thức khởi tạo của lớp cha

    # Ghi đè phương thức add_new_tile để tăng độ khó
    def add_new_tile(self):
        empty_cells = [(i, j) for i in range(4) for j in range(4) if self._board.get_grid_values()[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            # Thay vì chỉ thêm giá trị 2, ta có thể thêm cả giá trị 4 để tăng độ khó
            self._board.grid[i][j].set_value(random.choice([2, 4]))

# Sử dụng lớp Game2048HardMode
if __name__ == "__main__":
    root = tk.Tk()
    game = Game2048HardMode(root)  # Khởi tạo game với chế độ khó
    root.mainloop()

