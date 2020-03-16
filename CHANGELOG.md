# CHANGELOG

# Beta [v1.1] - 2020-03-??


### Added:

- Overhauled UI:
    - Added game instructions
    - Added colors!
    - Added instructions screen
    - Added difficulty selection screen
    - Changed the image background instead of foreground when selecting or confirming pieces
    - Updated piece images
    - Updated Icon
- Added more difficulty options 
(Note that the game get stuck at very hard or higher)
- Implemented symmetric gamestate detection (Starting options from 420 to 126)
    

### Changed:

- Moved from minimax to negamax algorithm
- Changed Option implementation so that the gamestate is stored as a numpy array

### Fixed:

- Fixed bug that crashed the program if the Main Menu/Reset
buttons were pressed multiple times
- Improved memory usage by using lower resolution image files


# Beta [v1.0] - 2020-03-03


### Added:

- Added Piece.\__str\__() method
- Documented methods

### Changed:

- Moved minimax function from minimax.py to board.py
- Renamed minimax.py to ai.py

## Fixed:

- Fixed multiplayer player string names
- Fixed AI bugs
- Improved code readability


## Alpha [v0.3] - 2020-02-11


### Added:
- Implemented confirm function
- Implemented evaluation function
- get_options sorts similar moves together and sorts groups of moves by score
- Added keyboard controls
- Refactored and documented code

### Changed:
- Replaced piece images with higher resolution versions
- Moved is_full function from minimax into board.Board
- Improved is_full efficiency by checking the number of pieces left in Board.pieces_bar rather than checking if every spot in the board isn't empty
- Moved pieces_set from Board to PiecesBar
- Fixed EndMessage errors and finished implementing it

### Removed:

- Removed redundant type checks in functions


# Pre-alpha [v0.2] - 2020-01-02


### Added:
- Implemented has_won, insert, insert_selected and reset functions

### Changed:
- Moved logs into /logs/ directory
- Changed background color of the playing board and pieces bar
- Redesigned pieces images so they look like they are in a tile and are easier to separate 
- Created a new class for the endgame message and moved its declaration to the .kv file
- Updated .gitignore
- Implemented more explicit error messages
- Minimax and it's helper functions now return an Option object
- Restructured multiple files
- Reformatted CHANGELOG

### Fixed:
- Fixed many bugs that prevented application from launching
- Changed GameScreen's main BoxLayout orientation to vertical instead of horizontal
- Changed the blank image so the game board looks more like the original Quarto game
- Fixed multiple typing module errors


# Pre-alpha [v0.1] - 2019-12-13


### Added:
- Added basic logging
- Added a kivy config file
- Added ScreenManager and the game's screens
- Added all function signatures

### Changed:
- Update .gitignore
- Refactored code
- Annotated functions
- Renamed 'enums.py' to 'constants.py'
- Fixed _some_ minor bugs (Code still doesn't run)
- Documented modules, classes and functions


## Pre-alpha [v0.0] - 2019-11-19


### Added:
- Added CHANGELOG.md
- Added README.md
- Added .gitignore
- Added MIT License
- Added CC 4.0 License for assets/
- Added credits.md file
- Added Icon
- Added piece images
- Added main script
- Created basic project structure
- Implemented most of src/minimax.py's functions
- Added pip requirements file (For windows)
