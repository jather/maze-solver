from tkinter import Tk, BOTH, Canvas


class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title = "maze-solver"
        self.__canvas = Canvas(self.__root, width=width, height=height)
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__running = True
        while self.__running == True:
            self.redraw()
        print("closing window")

    def close(self):
        self.__running = False

    def draw_line(self, line, fill_color="black"):
        line.draw(self.__canvas, fill_color)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line:
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2

    def draw(self, Canvas, fill_color):
        Canvas.create_line(
            self.point1.x,
            self.point1.y,
            self.point2.x,
            self.point2.y,
            fill=fill_color,
            width=2,
        )


class Cell:
    def __init__(self, window):
        self.walls = {"top": True, "left": True, "bottom": True, "right": True}
        self._win = window
        self._x1 = None
        self._x2 = None
        self._y1 = None
        self._y2 = None

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
        if self.walls["left"]:
            self._win.draw_line(Line(top_left, bottom_left))
        if self.walls["bottom"]:
            self._win.draw_line(Line(bottom_left, bottom_right))
        if self.walls["right"]:
            self._win.draw_line(Line(bottom_right, top_right))

    def draw_move(self, to_cell, undo=False):
        def find_center(cell):
            return Point((cell._x1 + cell._x2) // 2, (cell._y1 + cell._y2) // 2)

        line_color = "gray"
        if undo is False:
            line_color = "red"

        move_line = Line(find_center(self), find_center(to_cell))
        self._win.draw_line(move_line, line_color)
