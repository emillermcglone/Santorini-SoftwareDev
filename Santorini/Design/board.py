# This file describes the high-level interactions that a `GameBoard` will be responsible for


# A BoardDict is a:
#   wrapper class around a dict that will ensure that lookups
#   will not exceed the maximal board game coordinates

# A Cell is one of:
# - Worker, a class representing a worker game piece
# - Building, a class representing a building game piece
# - None, representing an empty Cell

# A TurnPhase is one of:
# - "PLACE", representing the initial piece placement phase
# - "MOVE", representing the move phase of a player's turn
# - "BUILD", representing the build phase of a player's turn

class GameBoard:
    """Class representing a Santorini game board

    Attributes:
        player1:        Unique string identifying player 1
        player2:        Unique string identifying player 2
        board:          A BoardDict mapping x,y values in the form of a tuple
                        to a Cell.
        turn_phase:     A TurnPhase
        turn_count:     An integer representing the current turn number
        game_over:      A boolean representing whether this GameBoard
                        is still playable
        winner:         A string representing the player that won on this board
                        None while not game_over
    """

    def __init__(self, player1_id, player2_id):
        """Initializes this GameBoard with default values

        Args:
            player1_id: Unique string identifying player 1
            player2_id: Unique string identifying player 2
        """
        pass

    def place_worker(self, pid, x, y):
        """Method to allow players to place workers onto the game board

        Places a Worker at the cell x,y

        Args:
            pid:        A string that represents a player
            x:          An integer representing the x coordinate
                        of the targeted board cell
            y:          An integer representing the y coordinate
                        of the targeted board cell

        Raises:
            IllegalPlaceError: You cannot place a worker at (x,y)
        """
        pass

    def move_worker(self, pid, x1, y1, x2, y2):
        """Method to allow players to move workers between board cells.

        Moves a worker from x1,y1 to x2,y2.

        Args:
            pid:        A string that represents a player
            x1:         An integer representing the x coordinate
                        of the source board cell
            y1:         An integer representing the y coordinate
                        of the source board cell
            x2:         An integer representing the x coordinate
                        of the destination board cell
            y2:         An integer representing the y coordinate
                        of the destination board cell

        Raises:
            IllegalMoveError: You cannot move a worker from (x1,y1) to (x2,y2)
        """

        pass

    def build_floor(self, pid, x1, y1, x2, y2):
        """Method to allow players to build a floor with a worker.

        Adds 1 height to the cell at x2,y2 using the worker at x1,y1.

        Args:
            pid:        A string that represents a player
            x1:         An integer representing the x coordinate
                        of the Worker board cell
            y1:         An integer representing the y coordinate
                        of the Worker board cell
            x2:         An integer representing the x coordinate
                        of the targeted board cell
            y2:         An integer representing the y coordinate
                        of the targeted board cell

        Raises:
            IllegalBuildError: You cannot use the worker at (x1,y1) to build on (x2,y2)
        """
        pass

    def get_cell(self, x, y):
        """Method to allow access to a particular Cell

        Looks up (x,y) in the board and returns the Cell

        Args:
            x:          An integer representing the x coordinate of
                        the Cell to get
            y:          An integer representing the y coordinate of
                        the Cell to get

        Returns:
            Cell at (x,y) in the board

        Raises:
            IllegalCellPositionError: There is no Cell at the given (x,y) value
        """
        pass

    def get_player(self, wid):
        """Method to get the x, y coordinates of the given Worker ID

        Iterates through the board dict looking for a Worker that has a matching ID

        Args:
            wid             A string that identifies the Worker to look up

        Returns:
            Tuple containing the x, y cooridnate of the Worker

        Raises:
            IllegalWorkerLookupError: There is no worker with the id wid
        """
        pass

    def get_player_turn(self):
        """Method to determine which player's turn it is

        Uses turn_count to determine which player's turn it currently is

        Returns:
            String identifying the current player's turn
        """
        pass

    def game_over(self, pid):
        """Method to alert the GameBoard that the game is over and who won

        Allows other game objects to alert the GameBoard that a player has won
        and that it should stop playing

        Args:
            pid:        A string identifying the winning player
        """
        pass

    def next_turn(self):
        """Method that hold logic for updating internal vars for next turn

        Used in the main game loop to update internal vars that track game
        state to progress the game to the next player's turn
        """
        pass

    def play(self):
        """Method that contains main game loop

        Called to start this GameBoard and begin playing
        """
        pass
