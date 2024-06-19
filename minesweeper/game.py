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

class Game:
    def __init__(self, start_row : int, start_col : int, rows : int, cols : int, density : float, seed : int):
        self.mine_map = self._generate_mine_map(start_row, start_col, rows, cols, density, seed)
        self.user_map = self._generate_user_view(rows, cols)


    def _generate_mine_map(self, start_row : int, start_col : int, rows : int, cols : int, density : float, seed : int) -> Map:
        map = [[self._randomly_pick_mine_or_empty(density, seed=seed) for _ in range(cols)] for _ in range(rows)]
        for i, j in self._adjacent_coordinates(start_row, start_col, map):        
            map[i][j] = Tile.EMPTY
        return map
    
    def _randomly_pick_mine_or_empty(self, density : float, seed = 100):
        assert density >= 0 and density <= 1
        return Tile.MINE if random.random() < density else Tile.EMPTY

    def _generate_user_view(self, rows : int, cols : int) -> Map:
        return [[Tile.HIDDEN for _ in range(cols)] for _ in range(rows)]

    def print_board(self) -> str:
        print(self._map_to_str(self.user_map))

    def _map_to_str(self, map : Map):
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

    def did_user_win(self) -> bool:
        for i, j in self._iterate_over_map(self.user_map):
            if self.user_map[i][j] == Tile.HIDDEN and not self.mine_map[i][j] == Tile.MINE:
                return False
        return True

    def reveal_hidden_mines(self):
        for i in range(0,len(self.user_map)):
            for j in range(0, len(self.user_map[0])):
                if self.mine_map[i][j] == Tile.MINE:                
                    self.user_map[i][j] = Tile.MINE


    def reveal_tile(self, row : int, col : int) -> bool:
        """
        First check if the revealed tile is a mine, if it is set to mine and return.

        First it counts the number of mines surrounding the tile

        If it is zero, reveal all the surrounding tiles. 

        If it is nonzero, set the tile to be NUMBER_OF_TILES
        """
        if self.mine_map[row][col] == Tile.MINE:
            self.user_map[row][col] == Tile.MINE
            return True

        num_surrounding_mines = self._count_number_of_mines_surrounding_tile(row, col,)
        self.user_map[row][col] = Tile(num_surrounding_mines)
        if num_surrounding_mines == 0:
            for i, j in self._adjacent_coordinates(row, col, self.mine_map):
                if self.user_map[i][j] == Tile.HIDDEN:
                    self.reveal_tile(i,j)        
        return False

    def _count_number_of_mines_surrounding_tile(self, row : int, col : int):
        num_mines = 0
        for i, j in self._adjacent_coordinates(row, col, self.mine_map):
            num_mines += int(self.mine_map[i][j] == Tile.MINE)
        return num_mines

    def _adjacent_coordinates(self, row : int, col :int, map : Map) -> Generator[Tuple[int, int], None, None]:
        for i in range(row-1, row+2):
            for j in range(col-1, col+2):
                if self._is_valid_coordinate(i,j, len(map), len(map[0])):
                    yield i, j

    def _iterate_over_map(self, map : Map):
        for i in range(len(map)):
            for j in range(len(map[0])):
                yield i, j

    def _is_valid_coordinate(self, row : int, col : int, rows : int, cols : int) -> bool:
        return row < rows and col < cols and row >= 0 and col >= 0
