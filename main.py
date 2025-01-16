from window import Window, Cell


def main():
    win = Window(800, 600)
    cell = Cell(win)
    cell.walls["top"] = False
    cell.draw(200, 250, 300, 350)
    other_cell = Cell(win)
    other_cell.draw(450, 350, 550, 450)
    cell.draw_move(other_cell)
    win.wait_for_close()


if __name__ == "__main__":
    main()
