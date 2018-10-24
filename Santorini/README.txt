=========================================================================================

Design and implementation progress of Santorini

=========================================================================================

Files:
    ├── Admin - Contains administrator-specific code
    ├── Common - Contains modules shared between player/administrative components
    │   ├── __init__.py - Empty python package initialization file
    │   ├── board.py - Model implementation for the game board
    │   ├── cell.py - Model for individual game cells
    │   ├── command_handler.py - Generic object to implement interpreter pattern
    │   ├── exception.py - Custom exceptions for the game
    │   ├── rule_checker.py - Model implementation for a rule checker
    │   ├── turn_phase.py - Enum for the various phases of turns in the game
    ├── Design - Contains design code and documentation
    │   ├── action_spec.txt - Valid actions that we use for internal turn representation
    │   ├── board.py - Stubs for the game board interface
    │   ├── plan.pdf - Design document for the Santorini game
    │   ├── player.py - Stubs for the player interface
    │   ├── referee.py - Stubs for the game referee interface
    │   ├── rule_checker.py - Stubs for the rule checker interface
    │   ├── strategy.py - Stubs for a strategy interface
    ├── Lib - Contains library code
    |   ├── stack_board.py - Class that allows us to interact with a GameBoard like a Stack
    |   ├── util.py - Holds some utility functions for general functions
    ├── Player - Contains player-specific code
    │   ├── __init__.py - Empty python package initialization file
    │   ├── board_parser.py - Parses board tests and does appropriate board operations
    |   ├── rule_parser.py - Parses rule tests and does appropriate rule operations
    │   ├── strategy_parser.py - Parses strategy tests and does appropriate operations
    │   ├── test_message_funcs.py - Contains functionality for test message spec
    │   ├── test_strategy_alive.py - Contains functionality for test strategy alive spec
    │   ├── test_strategy_place1.py - Functionality for strategy diagonal placement spec
    │   ├── test_strategy_palce2.py - Functionality for strategy furthest placement spec
=========================================================================================

09/24/2018
-----------------------------------------------------------------------------------------
Added board.py, a python source file that has stubbed out methods to be implemented for
what a game board for Santorni will look like and be responsible for. Some useful
additional context for the design is that we intend to have a Worker and Building class
that are each a type of Cell (see data def in board.PP) which wil further hold
information about the height of a Cell. It is also our current intent to have the Worker
class hold most of the game logic that governs movement and building.
-----------------------------------------------------------------------------------------

10/01/2018
-----------------------------------------------------------------------------------------
Added implementation for board.py, some changes were needed to implement all the
functionality required by the tests. Part of this implementation was implementing cells
and adding in additional files that help us define board state like turn_phase.py. To
implement the test harness a few new files were added, command_handler.py allows for
easy implementation of the interpreter pattern and can be reused. test_message_funcs.py
contains all the test-specific handling of the given JSON spec for testing, while
test_parser.py actually hooks them up together and can parse the test JSON. Finally for
the design task we added rule_checker.py and player.py that hold stubs for what we think
those classes should provide.
-----------------------------------------------------------------------------------------

10/08/2018
-----------------------------------------------------------------------------------------
Added implementation for rule_checker.py, this was actually kept very similar to our
initial design with the only difference being the removal of a game_over check as we are
still unsure where exactly this should happen in the game flow so we are leaving it
un-implemented for now. Building the test harness rules was very similar to the one for
a board with the main difference being state of the tests. State kept for move/build
sequencing is in 7/README.txt. There was additional state control that was needed in
actually invoking the rule_checker methods because things like player and worker id are
all things that need to be checked but we do not believe is the responsibility of the
rule_checker. Instead we would like these state components to be enforced by a higher
level Admin component that would be responsible for control flow of the actual game. In
order to appropriately test this we had the test functions mock up this functionality
that the rule_checker will rely on.

For the design task we have the strategy.py interface that shows how we expect to
interface with a strategy component. The main communication between this component and
the rest of our code should all happen over queues so that it can easily be hooked up to
a variety of communication pipes be they sockets, stdin/out or something we have not
envisioned. The use of JSON values over a queue allows for a 'loose' boundary that can
easily have some communication object inserted between the two.

Santorini/Common/rule_checker.py should be the main file to read for implementation
Santorini/Design/strategy.py should be the file to read for design work
-----------------------------------------------------------------------------------------

10/15/2018
-----------------------------------------------------------------------------------------
Added implementation for an example strategy. This took some doing and we re-worked how
we used a strategy object to be more generic. We formalized what internal turn actions
looked like for us in action_spec.txt and we use that to represent different actions.
This allowed us to view the actual transitions as our state space as we searched. That
along with stack_board.py allowed us to implement a fairly classic example of depth first
search to use on our game tree.

For the design task we kept it pretty simple as we have already built a lot of the
machinery that is needed to check whether a action is valid or not. We re used that in
the referee and just built a wrapper around a RuleChecker that would call the appropriate
function via a Cmd_Handler. We kept some additional state in the referee so that we could
immediately throw out an action if it was no the correct phase of the game for it

Santorini/Player/test_strategy_alive.py is the main file to read for implementation
Santorini/Player/test_strategy_place1.py implementation of one of the placement strats
Santorini/Player/test_strategy_place2.py implementation of one of the placement strats
Santorini/Lib/stack_board.py is supplementary but shows how we operate on a GameBoard
Santorini/Design/referee.py is the file for the design task
=========================================================================================



=========================================================================================

Change Log 

=========================================================================================

10/22/2018
-----------------------------------------------------------------------------------------
Problems:
- Player does not have data piped into it. There's no access to board, rules, or 
referee (if that's the intended design). 

- Strategy directly mutates the board. 
- Strategy has no access to the board it's supposed to operate on, unless the 'optional'
argument for a board is given in the constructor. This does not make sense for a component
that's supposed to plan actions based on current state of game. 
- Strategy methods return True or False depending on whether the action based on the
strategy has been enacted on the board. 
- Strategy has no reference to rule checker. It has the basic rules of Santorini baked into
its logic. 
- Strategy exposes private methods
- Interface is hopeless and not salvagable. It only delivers the needs of the testing 
harnesses and doesn't serve the purpose of planning next moves in a game. 

- Referee seems to be the "rule checker" for the player. It has a check method that checks
if given action is valid. 
- Referee has no way of exposing the current state of the game. Interface is very limited
to other components that manage or interact with it. 
- Referee does not have players piped into it. It almost seems like it has to access the 
players through the given board, which inverts the control of the game flow. 

- Implementation classes are not consistent with their interfaces in Design (e.g. board,
rule_checker, strategy)
- Implementation classes also don't "extend" the interfaces
- These interfaces/implementation classes seem to accomplish the needed testing tasks,
but have no forethought for the actual Santorini game. 

- Method signatures and purpose statements are inaccurate or incomplete. 

Solution:
- Fix literally every interface 

They've woken the psychopaths in us


Changes:
    Player Interface:
    - Place, move and build all take in a copy of the board game
    - Constructor takes in a RuleChecker

    RuleChecker Interface:
    - Replaced all methods with methods of provided implementation class so that
    rule checker has an instance of the board state at all times

    GameBoard Interface:
    - added find_player_workers to get all of given player's workers

    Referee Interface:
    - added run_game method to run a game through the referee


Added player.py in Player for player implementation.
- Use diagonal strategy for placement, and random strategy for move and build.

Added Observer.py in Design, which outlines the interface for a Santorini Observer.py

Issues:
- Action 'type' attribute should use given TurnPhase
- RuleChecker should have an interface to grab game constants such as
number of workers allowed on the game.
- check_game_over should not return None


-----------------------------------------------------------------------------------------