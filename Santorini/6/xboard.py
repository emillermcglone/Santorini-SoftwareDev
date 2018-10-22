#!/usr/bin/env python3.6
# File that sets up test harness and reads tests

import sys
# Add parent directory to path so that we can import from Santorini
sys.path.append('..')
import json
# import the needed parts from Santorini to run tests
from Player.board_parser import Board_Tester
from Lib.util import parse_json

# Parse out JSON commands on STDIN
cmds = parse_json()

# Instantiate the test parser
parser = Board_Tester()


# Take the first JSON which is the state of the board and set that up
parser.set_board(cmds[0])
# Go though the test JSON and take care of them one at a time
for j in cmds[1:]:
    print(json.dumps(parser.parse(j)))
