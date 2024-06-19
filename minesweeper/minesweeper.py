from minesweeper.map import *


def get_row_col_input() -> Tuple[int,int]:
    row = int(input("Which row to reveal?"))
    col = int(input("Which col to reveal?"))
    return (row, col)


def play():
    rows = int(input("How many rows?"))
    cols = int(input("How many cols?"))

    user_map = generate_user_view(rows, cols)

    row, col = get_row_col_input()

    mine_map = generate_mine_map(row, col, rows, cols, .5, 100)

    while not reveal_tile(row, col, user_map, mine_map) and not check_win(user_map, mine_map):
        print(create_map_output(user_map))        
        row, col = get_row_col_input()

    if check_win(user_map, mine_map):
        print("YOU WIN!")

    reveal_hidden_mines(user_map, mine_map)
    print(create_map_output(user_map))