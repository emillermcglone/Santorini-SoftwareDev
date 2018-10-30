For all Santorini changes please reference Santorini/README.txt for 10/15/2018

Added xstrategy which is an executable python file that setups up all the required
parts for running tests, getting JSON from STDIN and running the commands against
a board and printing the results

xstrategy works much the same way as xboard as far as dealing with JSON and dispatching
to a parser for strategy tests. It does some additional processing to pull out the relevant
state information that is given to us in order to appropriately setup the strategy object.

xstrategy is in this directory for review and relies on:
Santorini/Player/strategy_parser.py - For parsing the test messages
Santorini/Player/test_strategy_alive.py - For the actual strategy implementation
Santorini/Player/test_message_funcs.py - For the actual handling of the different test messages

To run tests run 'bash testme.sh' which will invoke xstrategy using python3 with all
the tests in the board-tests directory and output any diffs. testme.sh is also
executable but we would prefer you directly invoke it with bash to ensure that it
runs. This must be invoked from 8/ or else testme.sh will break.