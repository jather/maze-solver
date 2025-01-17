from window import Window
from maze import Maze, Cell


def main():
    win = Window(800, 600)
    maze = Maze(200, 200, 5, 5, 40, 40, win)
    maze.break_walls_r(0, 0)
    maze.reset_cells_visited()
    win.wait_for_close()


if __name__ == "__main__":
    main()
