For all Santorini changes please reference Santorini/README.txt for 10/08/2018

Added xrules which is an executable python file that setups up all the required
parts for running tests, getting JSON from STDIN and running the commands against
a board and printing the results

xrules works much the same way as xboard as far as dealing with JSON and dispatching
to a parser for rule tests. It does however do some additional processing to ensure that
a "move" and optional "+build" sequence are handled properly so that there is a single
result for the whole sequence. This is done here because in our implementation we have
separate checks for a move and build action respectively and we would expect that a player
component would want separate feedback for each action so combining the two for the sake
of tests seemed like a bad design choice.

xrules is in this directory for review and relies on:
Santorini/Player/rule_parser.py - For parsing the test messages
Santorini/Player/test_message_funcs.py - For the actual handling of the different test messages

To run tests run 'bash testme.sh' which will invoke xrules using python3 with all
the tests in the board-tests directory and output any diffs. testme.sh is also
executable but we would prefer you directly invoke it with bash to ensure that it
runs. This must be invoked from 7/ or else testme.sh will break.