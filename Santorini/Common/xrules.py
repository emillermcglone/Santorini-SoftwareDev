"""
Test harness for SantoriniRules
"""

import fileinput, io, sys, json, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from splitstream import splitfile
from functools import reduce
from Admin.action_board import ActionBoard
from Common.rules import SantoriniRules

from xboard import create_direction, create_cell

def create_board(state, request):
    """
    Translate test harness board to ActionBoard.

    :param state: {}, state of the turn action  
    :param request: [[Cell, ...], ...], the test harness board
    :return: IActionBoard, the query board
    """

    new_board = [[create_cell(c) for c in l] for l in request]
    state["action_board"] = ActionBoard(new_board)
    state["rules"] = SantoriniRules(state["action_board"].query_board)

def write(valid, output):
    """
    Write the output with a new line.

    :param valid: true | false, whether the turn action is valid or invalid
    """
    output.write(("yes" if valid else "no") + "\n")
    

def respond(state):
    """
    Respond to the requested action. 

    :param state: {}, state of the turn action
    """
    if state["move"] is None:
        return
    elif state["build"] is None:
        write(state["move"], state["output"])
    else:
        write(state["move"] and state["build"], state["output"])
    reset_state(state)

              
def move(state, request):
    """
    Check if the move request is valid and update the state.
    If the move is valid, move the worker in the direction given.

    :param state: {}, state of the turn action
    :param request: [String, String, String], the test harness check move request, worker, direction
    """
    worker = request[1]
    direction = create_direction(request[2])

    if state["rules"].check_move(worker, direction):
        state["action_board"].move(worker, direction)
        state["move"] = True
        state["moved_worker"] = worker
    else:
        state["move"] = False
        state["moved_worker"] = worker


def build(state, request):
    """
    Check if the build request is valid and update the state.

    :param state: {}, state of the turn action
    :param request: [String, String], the test harness check build request, direction
    """
    worker = state["moved_worker"]
    direction = create_direction(request[1])
    state["build"] = state["rules"].check_build(worker, direction)
    respond(state)


def handle_requests(state, request):
    """
    Handle the request, depending on whether it's check move, or check build. 

    :param state: {}, state of the turn action
    :param request: [String, String, String], the test harness check move request, worker, direction
    :param request: [String, String], the test harness check build request, direction
    """
    requests = { "move": move, "+build": build }
    requests[request[0]](state, request)


def reset_state(state):
    """
    Reset the state to None.

    :param state: {}, state of the turn action
    """
    state["action_board"] = None
    state["rules"] = None
    state["move"] = None
    state["build"] = None
    state["moved_worker"] = None


def main():
    output = open(sys.argv[2], 'w') if len(sys.argv) >= 3 else sys.stdout

    state = {
        "action_board": None,
        "rules": None,
        "move": None,
        "build": None,
        "moved_worker": None,
        "output": output
    }

    with fileinput.input() as f:
        inputs = reduce(lambda x, y: x + y, f)
        readable = io.BytesIO(inputs.encode())
        
        for json_input in splitfile(readable, format="json"):
            request = json.loads(json_input)
            if isinstance(request[0], list):
                respond(state)
                state["board"] = create_board(state, request)
            else:
                handle_requests(state, request)

    respond(state)
    output.close()
            
if __name__ == "__main__":
    main()