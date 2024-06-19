from minesweeper.game import *


def get_row_col_input() -> Tuple[int,int]:
    row = int(input("Which row to reveal?"))
    col = int(input("Which col to reveal?"))
    return (row, col)


def play():
    rows = int(input("How many rows?"))
    cols = int(input("How many cols?"))

    row, col = get_row_col_input()

    game = Game(row, col, rows, cols, .5, 100)

    while not game.reveal_tile(row, col) and not game.did_user_win():
        game.print_board()
        row, col = get_row_col_input()
    
    if game.did_user_win():
        print("YOU WIN!")

    game.reveal_hidden_mines()
    game.print_board()