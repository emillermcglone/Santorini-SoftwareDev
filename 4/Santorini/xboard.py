from splitstream import splitfile
from Design.board import Board
from Common.common.components import *

import fileinput, io, sys
import json

def create_board(board, rules):
    """
    Translate test harness board to Santorini board.

    :param board: [[Cell, ...], ...], the test harness board
    :param rules: [Rule, ...], the rules for the board
    :return: Board, instance of Santorini board
    """

    new_board = [[create_cell(c) for c in l] for l in board]
    return Board(rules, new_board)


def move(board, request, output):
    """
    Handle move request and empty JSON array to output.

    :param board: Board, the board
    :param request: [String, String, String], the test harness move request, worker, direction
    :param output: the output
    """

    worker = create_cell(request[1])
    direction = create_direction(request[2])
    board.move(worker.id, direction)
    output.write("[]")

def build(board, request, output):
    """
    Handle build request and write empty JSON array to output.

    :param board: Board, the board
    :param request: [String, String, String], the test harness build request, worker, direction
    :param output: the output
    """
    worker = create_cell(request[1])
    direction = create_direction(request[2])
    board.build(worker.id, direction)
    output.write("[]")

def neighbor(board, request, output):
    """
    Handle neighbor request and print out "yes" or "no".

    :param board: Board, the board
    :param request: [String, String, String], the test harness neighbor request, worker, direction
    :param output: the output
    """
    worker = create_cell(build_request[1])
    direction = create_direction(request[2])
    response = "yes" if board.neighbor(worker.id, direction) else "no"
    output.write(response)

def occupy(board, request, output):
    """
    Handle occupy request and print out "yes" or "no".

    :param board: Board, the board
    :param request: [String, String, String], the test harness occupy request, worker, direction
    :param output: the output
    """
    worker = create_cell(build_request[1])
    direction = create_direction(request[2])
    response = "yes" if board.occupied(worker.id, direction) else "no"
    output.write(response)

def height(board, request, output):
    """
    Handle height request and print the height.

    :param board: Board, the board
    :param request: [String, String, String], the test harness height request, worker, direction
    :param output: the output
    """
    worker = create_cell(build_request[1])
    direction = create_direction(request[2])
    response = board.height(worker.id, direction)
    output.write(response)


def create_cell(cell):
    """
    Create the appropriate cell instance that is one of Worker or Height.

    :param cell: String | N, a buildingworker or height 
    """
    if isinstance(cell, str):
        height = cell[0]
        worker_id = cell[1:]
        return Worker(height, worker_id)
    else:
        return Height(height)

def create_direction(direction):
    """
    Create the appropriate Direction for move or build.

    :param direction: [String, String], where the first string is one of: "EAST" "PUT" "WEST" 
    and the second is one of: "NORTH" "PUT" "SOUTH".
    """
    east_west = None
    north_south = None

    if direction[0] == "East":
        east_west = Direction.E
    elif direction[0] == "West":
        east_west = Direction.W

    if direction[1] == "North":
        north_south = Direction.N
    elif direction[1] == "South":
        north_south = Direction.S

    if east_west is None:
        return north_south
    elif north_south is None:
        return east_west
    else:
        return Direction.compose(east_west, north_south)

def main():
    output = sys.stdout

    with fileinput.input() as f:
        for line in f:
            readable = io.BytesIO(line.encode())
            for json_value in splitfile(readable, format="json"):
                req_type = json_value[0]
                if isinstance(req_type, list):
                    board = create_board(json_value)
                elif req_type == "move":
                    move(board, req_type, output)
                elif req_type == "build":
                    build(board, req_type, output)
                elif req_type == "neighbor":
                    neighbor(board, req_type, output)
                elif req_type == "occupy":
                    occupy(board, req_type, output)
                elif req_type == "height":
                    height(board, req_type, output)
            
