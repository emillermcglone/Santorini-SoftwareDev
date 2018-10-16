import copy, sys, os, fileinput, io, json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from splitstream import splitfile
from functools import reduce
from Admin.rules import SantoriniRules
from Lib.xboard import create_board, create_direction
from Lib.gametree import GameTree

def get_player_workers(board, player):
    workers = board.workers
    return list(filter(lambda w: player in w.id, workers))


def move_and_build(player, board, worker, move_direction, build_direction, rounds):
    query_board = board.query_board
    workers = get_player_workers(query_board, player)
    worker_ids = list(map(lambda w: w.id, workers))
    game_tree = GameTree(board, worker_ids, SantoriniRules(query_board))

    survived = game_tree.survive(player + str(worker), move_direction, build_direction, rounds)
    return "yes" if survived else "no"


def main():
    output = open(sys.argv[2], 'w') if len(sys.argv) >= 3 else sys.stdout
    player = ""
    worker = 0
    move_direction = None
    build_direction = None
    rounds = 0


    with fileinput.input() as f:
        
        inputs = reduce(lambda x, y: x + y, f)
        for request in get_jsons(inputs):
            if isinstance(request, str):
                player = request
            elif isinstance(request, int):
                rounds = request
            elif request[0] == "move":
                worker = request[1][-1:]
                move_direction = create_direction(request[2])
            elif request[0] == "+build":
                build_direction = create_direction(request[1])
            else:
                board = create_board(request)

    output.write(move_and_build(player, board, worker, move_direction, build_direction, rounds))

def get_jsons(string):
    jsons = []
    acc = ""
    for c in string:
        acc += c
        try:
            obj = json.loads(acc)
            acc = ""
            jsons.append(obj)
        except:
            continue
    return jsons


            
if __name__ == "__main__":
    main()