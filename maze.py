from window import Point, Line
import time
import random


class Cell:
    def __init__(self, win=None):
        self.walls = {"top": True, "left": True, "bottom": True, "right": True}
        self._win = win
        self._x1 = None
        self._x2 = None
        self._y1 = None
        self._y2 = None
        self.visited = False

    def draw(self, x1, y1, x2, y2):
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2

        top_left = Point(self._x1, self._y1)
        top_right = Point(self._x2, self._y1)
        bottom_left = Point(self._x1, self._y2)
        bottom_right = Point(self._x2, self._y2)
        if self.walls["top"]:
            self._win.draw_line(Line(top_left, top_right))
        else:
            self._win.draw_line(Line(top_left, top_right), fill_color="white")
        if self.walls["left"]:
            self._win.draw_line(Line(top_left, bottom_left))
        else:
            self._win.draw_line(Line(top_left, bottom_left), fill_color="white")
        if self.walls["bottom"]:
            self._win.draw_line(Line(bottom_left, bottom_right))
        else:
            self._win.draw_line(Line(bottom_left, bottom_right), fill_color="white")
        if self.walls["right"]:
            self._win.draw_line(Line(bottom_right, top_right))
        else:
            self._win.draw_line(Line(bottom_right, top_right), fill_color="white")

    def draw_move(self, to_cell, undo=False):
        def find_center(cell):
            return Point((cell._x1 + cell._x2) // 2, (cell._y1 + cell._y2) // 2)

        line_color = "gray"
        if undo is False:
            line_color = "red"

        move_line = Line(find_center(self), find_center(to_cell))
        self._win.draw_line(move_line, line_color)


class Maze:
    def __init__(
        self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None, seed=None
    ):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._cells = []
        self._create_cells()
        self._break_entrance_and_exit()
        if seed is not None:
            random.seed(seed)

    def _create_cells(self):
        for col in range(self._num_cols):
            self._cells.append([Cell(self._win) for row in range(self._num_rows)])
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        if self._win is None:
            return
        cell_x1 = self._x1 + i * self._cell_size_x
        cell_x2 = cell_x1 + self._cell_size_x
        cell_y1 = self._y1 + j * self._cell_size_y
        cell_y2 = cell_y1 + self._cell_size_y
        self._cells[i][j].draw(cell_x1, cell_y1, cell_x2, cell_y2)
        self._animate()

    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(0.1)

    def _break_entrance_and_exit(self):
        entrance_cell = self._cells[0][0]
        exit_cell = self._cells[self._num_cols - 1][self._num_rows - 1]
        entrance_cell.walls["left"] = False
        self._draw_cell(0, 0)
        exit_cell.walls["right"] = False
        self._draw_cell(self._num_cols - 1, self._num_rows - 1)

    def break_walls_r(self, i, j):
        current = self._cells[i][j]
        current.visited = True
        while True:
            to_visit = []
            top = (i, j - 1)
            bottom = (i, j + 1)
            left = (i - 1, j)
            right = (i + 1, j)

            if j > 0:
                if self._cells[i][j - 1].visited is False:
                    to_visit.append(top)
            if i > 0:
                if self._cells[i - 1][j].visited is False:
                    to_visit.append(left)
            if j < self._num_rows - 1:
                if self._cells[i][j + 1].visited is False:
                    to_visit.append(bottom)
            if i < self._num_cols - 1:
                if self._cells[i + 1][j].visited is False:
                    to_visit.append(right)

            if not to_visit:
                self._draw_cell(i, j)
                return
            next_cell_position = random.choice(to_visit)
            next_cell = self._cells[next_cell_position[0]][next_cell_position[1]]
            if next_cell_position == top:
                current.walls["top"] = False
                next_cell.walls["bottom"] = False
            if next_cell_position == left:
                current.walls["left"] = False
                next_cell.walls["right"] = False
            if next_cell_position == right:
                current.walls["right"] = False
                next_cell.walls["left"] = False
            if next_cell_position == bottom:
                current.walls["bottom"] = False
                next_cell.walls["top"] = False
            self.break_walls_r(next_cell_position[0], next_cell_position[1])

    def reset_cells_visited(self):
        for col in self._cells:
            for cell in col:
                cell.visited = False

    def solve(self):
        return self._solve_r(i=0, j=0)

    def _solve_r(self, i, j):
        self._animate()
        if i == self._num_cols - 1 and j == self._num_rows - 1:
            return True
        current = self._cells[i][j]
        current.visited = True
        # mark as visited

        # check all 4 squares around:
        #   if exists, if no walls, and if not visited, add to list
        next_cells = []
        if (
            j > 0
            and self._cells[i][j - 1].visited is False
            and current.walls["top"] is False
        ):
            next_cells.append((i, j - 1))
        if (
            i > 0
            and self._cells[i - 1][j].visited is False
            and current.walls["left"] is False
        ):
            next_cells.append((i - 1, j))
        if (
            j < self._num_rows - 1
            and self._cells[i][j + 1].visited is False
            and current.walls["bottom"] is False
        ):
            next_cells.append((i, j + 1))
        if (
            i < self._num_cols - 1
            and self._cells[i + 1][j].visited is False
            and current.walls["right"] is False
        ):
            next_cells.append((i + 1, j))

        # for each cell in list:
        # draw line to next cell
        # recursively call, and if false draw undo line to next cellj
        for next_cell in next_cells:
            current.draw_move(self._cells[next_cell[0]][next_cell[1]])
            next_cell_success = self._solve_r(next_cell[0], next_cell[1])
            if next_cell_success:
                return True
            else:
                current.draw_move(self._cells[next_cell[0]][next_cell[1]], undo=True)

        # if still here, then return false
        return False
