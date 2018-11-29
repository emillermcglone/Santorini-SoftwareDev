# File containing utility functions
import json
import sys
import importlib.util
import fileinput
import pprint

def stdin():
    """
    Read all lines from fileinput.

    :return: string, input from fileinput
    """
    lines = ""
    for line in fileinput.input():
        lines += line
    return lines
    

def make_action(wid, move_action, build_action):
    move_from_xy = move_action['xy1']
    move_to_xy = move_action['xy2']

    build_from_xy = build_action['xy1']
    build_to_xy = build_action['xy2']

    move_direction = __get_direction(move_from_xy, move_to_xy)
    build_direction = __get_direction(build_from_xy, build_to_xy)
    return str([wid, *move_direction, *build_direction])


def __get_direction(from_xy, to_xy):
    from_x, from_y = from_xy
    to_x, to_y = to_xy
    
    return [__east_west(from_x, to_x), __north_south(from_y, to_y)]

    
def __north_south(from_y, to_y):
    if to_y is from_y:
        return "PUT"
    elif to_y > from_y:
        return "SOUTH"
    else:
        return "NORTH"

def __east_west(from_x, to_x):
    if to_x is from_x:
        return "PUT"
    elif to_x > from_x:
        return "EAST"
    else:
        return "WEST"


def xboard(board):
    json_board = [[cell(board.get_height(x, y), board.get_player_id(x, y), board.get_worker_id(x, y)) for x in range(6)] for y in range(6)]
    return pprint.pformat(json_board) + "\n"


def cell(height, player_id, worker_id):
    if player_id is None:
        return height
    return "{}{}{}".format(height, player_id, worker_id)

def make_place(wid, x, y):
    """
    Make a PLACE specification

    :param wid: string, worker id
    :param x: N, x coordinate
    :param y: N, y coordinate
    :return: PLACE, place specification
    """
    return { 
        'type': 'place',
        'wid': wid,
        'xy': [x, y]
    }


def make_move(x1, y1, x2, y2):
    """
    Make a MOVE specification

    :param x1: N, from x coordinate
    :param y1: N, from y coordinate
    :param x2: N, to x coordinate
    :param y2: N, to y coordinate
    :return: MOVE, move specification
    """
    return {
        'type': 'move',
        'xy1': [x1, y1],
        'xy2': [x2, y2],
    }


def make_build(x1, y1, x2, y2):
    """
    Make a BUILD specification

    :param x1: N, from x coordinate
    :param y1: N, from y coordinate
    :param x2: N, to x coordinate
    :param y2: N, to y coordinate
    :return: BUILD, build specification
    """
    return {
        'type': 'build',
        'xy1': [x1, y1],
        'xy2': [x2, y2],
    }


def path_import(absolute_path):
   spec = importlib.util.spec_from_file_location(absolute_path, absolute_path)
   module = importlib.util.module_from_spec(spec)
   spec.loader.exec_module(module)
   return module


def import_cls(path):
    """
    Dynamically load a class from a string path.

    :param path: string, path to python class
    :return: cls, python class
    """
    return path_import(path)


def parse_json():
    """
    Parse arbitrary JSON input into a list of JSON
    """
    # Storage var for all input
    input = ''
    # Read STDIN until EOF then flush to input
    for line in sys.stdin:
        input += line

    # Loop variable
    cur_json = ''
    total_json = []
    term_char = None

    # Go through input one character at a time
    for char in input:
        # Determine what character denotes the end of the current JSON value
        if term_char is None:
            # Check object, array, string, "true", "false", "null"
            if char == '{':
                term_char = '}'
            elif char == '[':
                term_char = ']'
            elif char == '\"':
                term_char = '\"'
            # Check for number
            elif not char == '\n':
                try:
                    int(char)
                    term_char = '\n'
                except ValueError as e:
                    raise ValueError('invalid JSON?: {}'.format(input))

        # Dont add newline to the current JSON we are collecting
        if not char == '\n':
            cur_json += char

        # Check to see if we are at a terminating char
        if char == term_char:
            # Check to see if we have built a valid piece of JSON
            try:
                total_json.append(json.loads(cur_json))
                # If the above does not raise an error we have valid JSON, reset
                cur_json = ''
                term_char = None
            except ValueError as e:
                pass

    # If we still have left over JSON after we have scanned all of `input`
    if not cur_json == '':
        raise ValueError('Left over incomplete JSON: \'{}\''.format(cur_json))

    return total_json


def check_distance(x1, y1, x2, y2):
    """
    Returns if the distance is within 1 unit

    :param x1: Represents the x coordinate of the first point
    :type x1: int
    :param y1: Represents the y coordinate of the first point
    :type y1: int
    :param x2: Represents the x coordinate of the second point
    :type x2: int
    :param y2: Represents the y coordinate of the second point
    :type y2: int
    :return: The distance between the two coordinates
    :rtype float
    """
    return abs(x1-x2) <= 1 and abs(y1-y2) <= 1


def gen_builds(player, w, board, checker):
    """
    Generate all valid builds for a worker
    :param player: Player ID
    :param w: worker as (x, y)
    :param board: a GameBoard
    :param checker: a RuleChecker
    :yield: a build action
    """
    for cell in get_adjacent(w[0], w[1]):
        wid = board.get_worker_id(*w)
        if checker.check_build(player, wid, w[0], w[1], cell[0], cell[1]):
            action = {'type': 'build', 'xy1': [w[0], w[1]], 'xy2': [cell[0], cell[1]], 'p': player}
            yield action


def gen_moves(player, board, checker):
    """
    Generate all valid moves for a worker
    :param player: Player ID
    :param board: a GameBoard
    :param checker: a RuleChecker
    :yield: a move action
    """
    workers = []

    for cell in board.find_workers():
        if board.get_player_id(cell[0], cell[1]) == player:
            workers.append(cell)

    for w in workers:
        for cell in get_adjacent(w[0], w[1]):
            if checker.check_move(player, w[0], w[1], cell[0], cell[1]):
                action = {'type': 'move', 'xy1': [w[0], w[1]], 'xy2': [cell[0], cell[1]], 'p': player}
                yield action


def get_adjacent(x, y):
    """
    Gets a list of coordinate tuples adjacent to the given coordinates

    :param x: Represents the x coordinate of the target board cell
    :type x:  int
    :param y: Represents the y coordinate of the target board cell
    :type y:  int
    :return:  The coordinate tuples adjacent to the given coordinates
    :rtype:   List[Tuple[int, int]]
    """
    return [(x + 1, y), (x + 1, y + 1), (x + 1, y - 1),
            (x, y - 1), (x, y + 1), (x - 1, y),
            (x - 1, y + 1), (x - 1, y - 1)]
