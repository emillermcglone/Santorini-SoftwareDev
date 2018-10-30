For all Santorini changes please reference Santorini/README.txt for 10/01/2018

Added xboard which is an executable python file that setups up all the required
parts for running tests, getting JSON from STDIN and running the commands against
a board and printing the results

To run tests run 'bash testme' which will invoke xboard using python3 with all
the tests in the board-tests directory and output any diffs. testme is also 
executbale but we would prefer you directly invoke it with bash to ensure that it 
runs This must be invoked from 6/ or else testme will break.
