# python-minesweeper

This project implements minesweeper in python.

I will decouple the ui from the logic of the game.

I will first implement the logic, and then I will implement the UI.

The interface of the UI to the backend will be a board object.

I think the general workflow of the game should be...

- select game options
- generate board
- play
- done screen with retry button. loops back to select game options.

When I generate the board, I should

- pick random places for the bombs
- do a

generate functions to make the board

board class that contains a board with all of the information

- where bombs are
- number of bombs next to a cell

then a separate grid class containing the information the user should be able to see. A boolean 2d array.

This can be encapsulated in a minesweeper board class.

- has two interfaces, get_board and check.
- check reveals a new tile on the board
- get_board returns the whole board

check should be renamed, reveal tile.

- reveal tile will return whether or not there was a bomb found.

after a bomb is found, the game should terminate.

To determine what is in a tile, I will use an enum. This enum will be the interface between the business logic and the ui. It will be how they communicate.

Ok new thought, lets just start programming, I don't even know when to use object oriented concepts versus functional concepts to achieve a goal.

I think that I'll just code and see what happens.

I read online today that someone see using functions as writing a DSL to solve their own problem. That makes a lot of sense to me.
