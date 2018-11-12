# Reworked Code 

* Reordered methods according to top down order
	* In referee, reorded the methods to have the most important at the top. 

* Refactored referee's check method and abstracted some code out
	* Added the helper, get_turn_phase, to the referee to simplify the check 
	method. 
	* Renamed the BreakingPlayer exception to BrokenPlayer.

* Implemented GuardedPlayer
	* Implement a guarded player for the referee to interact with. The guarded
	 player delegates all functionalities to the given external player, 
	 but will ensure that the player's id is kept constant throughout a 
	 game/series of games.

* Changed referee's internal use of Player to GuardedPlayer
	* Made changes to the referee to use the GuardedPlayer

* rule checker methods take in player id to validate actions
	* The rule checker methods, check_move and check_build, now take in the 
	player's id to check that the worker position that they have given in their 
	Action is the position of one of that player's workers. 
	* Updated corresponding method calls in other files to account for this change.

* Moved constants to a separate constants file. Will be updated along the way
	* In referee, the game win and lose messages are now message constants stored 
	in Admin.constants.py 
	* This file will be updated as we come across other constants that should be 
	moved to this file. 

* Check build takes in wid to validate that given position is given wid
	* The rule checker method, check_build, checks that the worker position given in 
	the build action is the same worker that they moved in their move action. 

* Fixed all uses of rule checker's check_build
	* Updated corresponding method calls in other files to account for this change.

* Abstracted observer functionality to ObserverManager and GuardedPlayer
	* Implemented an observer manager to manage all communication to observers. 
	* The place/move/build history of the player is kept in the guarded player 
	instead of in the referee. Turn history is needed explicitly for updating 
	the observers, so the referee should not need to have any interaction with it. 
	* The change_duplicate_ids method in the tournament manager now gives the player 
	an id that is all lower case. 



