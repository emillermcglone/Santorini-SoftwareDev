# Reworked Code 

* Reordered methods according to top down order
	* In Referee, reordered the methods according to visibility and then first appearance in the code. 

* Refactored Referee's check method and abstracted some code out
	* Added the helper, get_turn_phase, to the Referee to simplify the check method. 
	* Renamed the BreakingPlayer exception to BrokenPlayer.

* Implemented GuardedPlayer
	* Implemented a guarded player as an intermediary between the admin and the external player. It delegates all core functionalities to the given external player, but ensures that the player's id is kept constant throughout a game/series of games.
	* GuardedPlayer keeps track of player's action histories. This is a convenience query functionality that is useful for the ObserverManager, which extracts the information to update the observers.

* Changed Referee's internal use of Player to GuardedPlayer
	* Made changes to the Referee to use the GuardedPlayer

* RuleChecker methods take in player id to validate actions
	* The RuleChecker methods, check_move and check_build, now take in the 
	player's id to check that the worker position that they have given in their 
	Action is the position of one of that player's workers. 
	* Updated corresponding method calls in other files to account for this change.
	* This fix makes the Referee more robust and less prone to Player tampering.

* Moved constants to a separate constants file. Will be updated along the way
	* In Referee, the game win and lose messages are now message constants stored 
	in Admin.constants.py 
	* This file will be updated as we come across other constants that should be 
	moved to this file. 
	* For now, we won't move constants in the code written by the original authors to this file.

* Check build takes in wid to validate that given position is given wid
	* The RuleChecker method, check_build, checks that the worker position given in 
	the build action is the same worker that they moved in their move action. 

* Fixed all uses of RuleChecker's check_build
	* Updated corresponding method calls in other files to account for this change.

* Abstracted observer functionality to ObserverManager and GuardedPlayer
	* Implemented an ObserverManager to manage all communication to observers. 
	* The place/move/build history of the player is kept in the guarded player 
	instead of in the Referee. Turn history is needed explicitly for updating 
	the observers, so the Referee should not need to have any direct interaction with it.
	* The change_duplicate_ids method in the tournament manager now gives the player 
	an id that is all lower case.

* Cleaned up Referee by abstracting out methods
	* Extended GameOver to Exception. This makes the flow within Referee much more controllable, but not sure if it's the best design. This way however, the run_steady_phase method is much cleaner, inevitable code duplication is avoided, and the code makes more sense. 
	* Broke the __act method into separate parts for place, move, and build.


* Updated tests
	* side irrelevant change: ObserverManager no longer takes in a board
	* Fixed test_referee to deem random_two as winner


* Readded pid and wid to check methods in RuleChecker
	* Previous commit regarding adding pid and wid caused a lot of bugs. Had to remove the changes before and refactor the code again for this commit.


* ObserverManager purpose
	* Purpose statement for ObserverManager


* GuardedPlayer purpose
	* Purpose statement for GuardedPlayer


* Moved where observers are updated about game over in steady phase
	* ObserverManager is updated at the end of run_steady_phase method instead of raise_game_over.


* Fixed tournament reset
	* At the end of a series, the order of players doesn't go back to its original player. Now every series resets not just after every game, but also after each series.


* conftest.py file
	* Abstracted all common pytest fixtures into a single file for access by every test file.


* GuardedPlayer tests
	* Wrote tests for GuardedPlayer.

* Admin tests
	* Finished tests for all admin components.


* Refactoried tournament_manager, abstracting out code into separate methods
	* Removed code duplication
	* Abstracted out code into separate methods for readability and reduced method length.



