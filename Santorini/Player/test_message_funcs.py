# Holds all the functions for how the test harness will handle the different input messages
from Common.exception import *
from Common.turn_phase import TurnPhase


def convert_direction(dir):
    """
    Converts from Direction to a (x,y) delta
    """
    ew = dir[0]
    ns = dir[1]

    dx = 0
    dy = 0

    if ew == "EAST":
        dx = 1
    elif ew == "WEST":
        dx = -1

    if ns == "NORTH":
        dy = -1
    elif ns == "SOUTH":
        dy = 1

    return (dx, dy)


def split_worker_str(wstr):
    """
    Splits up a Worker into usable parts
    """
    worker_number = int(wstr[-1])
    player_id = wstr[:len(wstr) - 1]

    return (player_id, worker_number)


def build_board(cmd, client):
    """
    Builds a board given [[Cell, ...], ...] from spec
    """
    for j in range(len(cmd)):
        for i in range(len(cmd[j])):
            cell = cmd[j][i]
            if isinstance(cell, str):
                height = int(cell[:1])
                pid = cell[1:len(cell)-1]
                wid = int(cell[-1])
                client.board.place_worker(pid, wid, i, j)
                for _ in range(height):
                    client.board.build_floor(i, j)
            elif isinstance(cell, int):
                for _ in range(cell):
                    client.board.build_floor(i, j)


def board_move(cmd, client):
    """
    Moves a worker
    """
    pid, wid = split_worker_str(cmd[1])
    wx, wy = client.board.find_worker(pid, wid)
    dx, dy = convert_direction(cmd[2])
    tx = wx + dx
    ty = wy + dy

    try:
        #rule_checker.check_move(pid, client.board, wx, wy, tx, ty)
        client.board.move_worker(wx, wy, tx, ty)
    except IllegalMoveException as e:
        return False

    return []


def board_build(cmd, client):
    """
    Adds a single height value to the height of a cell
    """
    pid, wid = split_worker_str(cmd[1])
    wx, wy = client.board.find_worker(pid, wid)
    dx, dy = convert_direction(cmd[2])
    tx = wx + dx
    ty = wy + dy

    try:
        #rule_checker.check_build(pid, client.board, wx, wy, tx, ty)
        client.board.build_floor(tx, ty)
    except IllegalBuildException as e:
        return False

    return []


def neighbors_func(cmd, client):
    """
    Checks to see if there is a cell at a specific point
    """
    pid, wid = split_worker_str(cmd[1])
    wx, wy = client.board.find_worker(pid, wid)
    dx, dy = convert_direction(cmd[2])
    tx = wx + dx
    ty = wy + dy

    if (0 <= tx < 6) and (0 <= ty < 6):
        return "yes"
    else:
        return "no"


def occupied_func(cmd, client):
    """
    Checks to see if a cell is occupied by another worker
    """
    pid, wid = split_worker_str(cmd[1])
    wx, wy = client.board.find_worker(pid, wid)
    dx, dy = convert_direction(cmd[2])
    tx = wx + dx
    ty = wy + dy

    if client.board.get_player_id(tx, ty):
        return "yes"
    else:
        return "no"


def height_func(cmd, client):
    """
    Gets the height of a specific cell
    """
    pid, wid = split_worker_str(cmd[1])
    wx, wy = client.board.find_worker(pid, wid)
    dx, dy = convert_direction(cmd[2])
    tx = wx + dx
    ty = wy + dy

    return client.board.get_height(tx, ty)


def rule_move(cmd, client):
    """
    Checks to see if a move is valid and if so does it
    """
    pid, wid = split_worker_str(cmd[1])
    wx, wy = client.board.find_worker(pid, wid)
    dx, dy = convert_direction(cmd[2])
    tx = wx + dx
    ty = wy + dy

    client.checker.current_player = pid
    client.checker.current_worker = wid
    client.checker.current_phase = TurnPhase.MOVE

    if client.checker.check_move(pid, wx, wy, tx, ty):
        client.board.move_worker(wx, wy, tx, ty)
        client.checker.current_phase = TurnPhase.BUILD
        return "yes"
    else:
        return "no"


def rule_build(cmd, client):
    """
    Checks to see if a build is valid and if so does it
    """
    pid = client.checker.current_player
    wid = client.checker.current_worker
    wx, wy = client.board.find_worker(pid, wid)
    dx, dy = convert_direction(cmd[1])
    tx = wx + dx
    ty = wy + dy

    if client.checker.check_build(pid, wid, wx, wy, tx, ty):
        client.board.build_floor(tx, ty)
        return "yes"
    else:
        return "no"


def strat_move(cmd, client):
    """
    Moves a worker
    """
    pid, wid = split_worker_str(cmd[1])
    wx, wy = client.board.find_worker(pid, wid)
    dx, dy = convert_direction(cmd[2])
    tx = wx + dx
    ty = wy + dy
    client.prev_move = [tx, ty]

    client.strategy.get_result({'type': 'move', 'xy1': [wx, wy], 'xy2': [tx, ty]})


def strat_build(cmd, client):
    """
    Moves a worker
    """
    wx, wy = client.prev_move
    dx, dy = convert_direction(cmd[1])
    tx = wx + dx
    ty = wy + dy

    if client.strategy.get_result({'type': 'build', 'xy1': [wx, wy], 'xy2': [tx, ty]}):
        return "yes"
    else:
        return "no"