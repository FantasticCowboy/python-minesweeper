from enum import Enum
from typing import List, Generator, Tuple
import random



class Tile(Enum):
    HIDDEN = -3 # If the user cannot see the tile yet
    EMPTY = -2 # If the player reveals an empty time, all adjacent empty tiles will be revealed
    MINE = -1 
    ZERO_NEIGHBORING_MINES = 0
    ONE_NEIGHBORING_MINE = 1
    TWO_NEIGHBORING_MINES = 2
    THREE_NEIGHBORING_MINES = 3
    FOUR_NEIGHBORING_MINES = 4
    FIVE_NEIGHBORING_MINES = 5
    SIX_NEIGHBORING_MINES = 6
    SEVEN_NEIGHBORING_MINES = 7
    EIGHT_NEIGHBORING_MINES = 8

Map = List[List[Tile]]

def randomly_pick_mine_or_empty(density : float, seed = 100):
    assert density >= 0 and density <= 1
    return Tile.MINE if random.random() < density else Tile.EMPTY


def generate_mine_map(start_row : int, start_col : int, rows : int, cols : int, density : float, seed : int) -> Map:
    map = [[randomly_pick_mine_or_empty(density, seed=seed) for _ in range(cols)] for _ in range(rows)]
    for i, j in adjacent_coordinates(start_row, start_col, map):        
        map[i][j] = Tile.EMPTY
    return map

def generate_user_view(rows : int, cols : int) -> Map:
    return [[Tile.HIDDEN for _ in range(cols)] for _ in range(rows)]

def create_map_output(map : Map):
    output = ""
    for i in range(len(map)):
        for j in range(len(map[0])):
            if map[i][j] == Tile.HIDDEN:
                    output += "H"
            elif map[i][j] == Tile.EMPTY or map[i][j] == Tile.ZERO_NEIGHBORING_MINES:
                    output += "0"
            elif map[i][j] == Tile.MINE:                    
                    output += "X"
            else:
                output += str(map[i][j].value)
        output += "\n"
    return output

def check_win(user_map : Map, mine_map : Map):
    for i, j in iterate_over_map(user_map):
        if user_map[i][j] == Tile.HIDDEN and not mine_map[i][j] == Tile.MINE:
            return False
    return True

def reveal_hidden_mines(user_map : Map, mine_map : Map):
    for i in range(0,len(user_map)):
        for j in range(0, len(user_map[0])):
            if mine_map[i][j] == Tile.MINE:                
                user_map[i][j] = Tile.MINE


def reveal_tile(row : int, col : int, user_map : Map, mine_map : Map ) -> bool:
    """
    First check if the revealed tile is a mine, if it is set to mine and return.

    First it counts the number of mines surrounding the tile

    If it is zero, reveal all the surrounding tiles. 

    If it is nonzero, set the tile to be NUMBER_OF_TILES
    """
    if mine_map[row][col] == Tile.MINE:
        user_map[row][col] == Tile.MINE
        return True

    num_surrounding_mines = count_number_of_mines_surrounding_tile(row, col, mine_map)
    user_map[row][col] = Tile(num_surrounding_mines)
    if num_surrounding_mines == 0:
        for i, j in adjacent_coordinates(row, col, mine_map):
            if user_map[i][j] == Tile.HIDDEN:
                reveal_tile(i,j,user_map, mine_map)        
    return False

def count_number_of_mines_surrounding_tile(row : int, col : int, mine_map : Map):
    num_mines = 0
    for i, j in adjacent_coordinates(row, col, mine_map):
        num_mines += int(mine_map[i][j] == Tile.MINE)
    return num_mines

def adjacent_coordinates(row : int, col :int, mine_map : Map) -> Generator[Tuple[int, int], None, None]:
    for i in range(row-1, row+2):
        for j in range(col-1, col+2):
            if is_valid_coordinate(i,j, len(mine_map), len(mine_map[0])):
                yield i, j

def iterate_over_map(map : Map):
    for i in range(len(map)):
        for j in range(len(map[0])):
            yield i, j

def is_valid_coordinate(row : int, col : int, rows : int, cols : int) -> bool:
    return row < rows and col < cols and row >= 0 and col >= 0
