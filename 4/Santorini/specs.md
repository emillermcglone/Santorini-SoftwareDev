_Santorini_ is a 6 x 6 board. It knows what object is on each cell (_Floor_/_Worker_ and its altitude),
can update each cell by stacking up _Floors_, and (dis)placing a _Worker_. Restrictions regarding moves
are preserved by this class. This class also knows the _Players_ in the game and whose turn it is next, 
and signals which _Player_ wins. 

_Player_ has a name
_Worker_ has a player for identification
_Floor_ is an empty class