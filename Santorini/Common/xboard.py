#!/usr/bin/python3.4

import fileinput, io, sys
import json


from splitstream import splitfile
from components import *
from santorini import SantoriniBoard


def create_board(board, rules):
    """
    Translate test harness board to Santorini board.

    :param board: [[Cell, ...], ...], the test harness board
    :param rules: [Rule, ...], the rules for the board
    :return: Board, instance of Santorini board
    """

    new_board = [[create_cell(c) for c in l] for l in board]
    return SantoriniBoard(rules, new_board)


def move(board, request, output):
    """
    Handle move request and empty JSON array to output.

    :param board: Board, the board
    :param request: [String, String, String], the test harness move request, worker, direction
    :param output: the output
    """

    worker = request[1]
    direction = create_direction(request[2])
    try:
        board.move(worker, direction)
        output.write("[]\n")
    except:
        return

def build(board, request, output):
    """
    Handle build request and write empty JSON array to output.

    :param board: Board, the board
    :param request: [String, String, String], the test harness build request, worker, direction
    :param output: the output
    """
    
    worker = request[1]
    direction = create_direction(request[2])
    try:
        board.build(worker, direction)
        output.write("[]\n")
    except:
        return

def neighbor(board, request, output):
    """
    Handle neighbor request and print out "yes" or "no".

    :param board: Board, the board
    :param request: [String, String, String], the test harness neighbor request, worker, direction
    :param output: the output
    """
    worker = request[1]
    direction = create_direction(request[2])
    try:
        response = "yes" if board.neighbor(worker, direction) else "no"
    except:
        response = "no"
    output.write(response + "\n")


def occupy(board, request, output):
    """
    Handle occupy request and print out "yes" or "no".

    :param board: Board, the board
    :param request: [String, String, String], the test harness occupy request, worker, direction
    :param output: the output
    """
    worker = request[1]
    direction = create_direction(request[2])
    try:
        response = "yes" if board.occupied(worker, direction) else "no"
    except:
        response = "no"
    output.write(response + "\n")

def height(board, request, output):
    """
    Handle height request and print the height.

    :param board: Board, the board
    :param request: [String, String, String], the test harness height request, worker, direction
    :param output: the output
    """
    worker = request[1]
    direction = create_direction(request[2])
    try:
        response = str(board.height(worker, direction))
    except:
        response = str(0)
    output.write(response + "\n")


def create_cell(cell):
    """
    Create the appropriate cell instance that is one of Worker or Height.

    :param cell: String | N, a buildingworker or height 
    """
    if isinstance(cell, str):
        height = int(cell[0])
        worker_id = cell[1:]
        return Worker(worker_id, height)
    else:
        return Height(cell)

def create_direction(direction):
    """
    Create the appropriate Direction for move or build.

    :param direction: [String, String], the test harness directions
    """

    directions = {
        "EAST": Direction.E, 
        "WEST": Direction.W,
        "NORTH": Direction.N,
        "SOUTH": Direction.S,
        "PUT": lambda x, y: (x, y)
    }

    east_west = directions[direction[0]]
    north_south = directions[direction[1]]

    return Direction.compose(east_west, north_south)


def handle_requests(board, request, output):
    requests = {
        "move": move,
        "build": build,
        "neighbor": neighbor,
        "occupy": occupy,
        "height": height,
    }

    requests[request[0]](board, request, output)


def main():
    output = open(sys.argv[2], 'w') if len(sys.argv) >= 3 else sys.stdout
    board = [[]]

    with fileinput.input() as f:
        inputs = ""
        for line in f:
            inputs += line
        
        readable = io.BytesIO(inputs.encode())
        
        for json_input in splitfile(readable, format="json"):
            request = json.loads(json_input)
            if isinstance(request[0], list):
                board = create_board(request, Rules([], []))
            else:
                handle_requests(board, request, output)

    output.close()
            
if __name__ == "__main__":
    main()
