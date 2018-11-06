# File containing utility functions
import json
import sys
import importlib

def import_cls(path):
    """
    Dynamically load a class from a string path.

    :param path: string, path to python class
    :return: cls, python class
    """

    class_data = path.split(".")
    module_path = ".".join(class_data[:-1])
    class_str = class_data[-1]

    module = importlib.import_module(module_path)
    
    return getattr(module, class_str)


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
        if checker.check_build(w[0], w[1], cell[0], cell[1]):
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
            if checker.check_move(w[0], w[1], cell[0], cell[1]):
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
