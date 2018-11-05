
import json

import sys, os
sys.path.append('./Santorini/')
sys.path.append('./gija-emmi/Santorini/')
sys.path.append('../Santorini/')


from Design.observer import IObserver
from enum import Enum
from timeout_decorator import timeout, TimeoutError

from Admin.referee import Referee
from Player.mock_players.random_player import Player
from Player.mock_players.infinite_loop_player import InfiniteLoopPlayer
from Player.mock_players.misbehaving_player import MisbehavingPlayer


class XObserver(IObserver):
    """
    Observer that prints out updates from Referee to given output. 

    The order of updates is as follows:
    - state of board after 4 placements
    - action taken of each player, either a move or a build
    - state of board after action
    - winner of game

    Status for players giving up or making errors can be printed out anytime 
    and winner of game will be announced.
    """


    def __init__(self, output=sys.stdout):
        """
        Initialize observer with output.

        :param output: writable output defaulted to STDOUT
        """
        self.output = output


    def update_state_of_game(self, board):
        json_board = [[self.__cell(board.get_height(x, y), board.get_player_id(x, y), board.get_worker_id(x, y)) for x in range(6)] for y in range(6)]
        self.write_to_output(json_board)


    def update_action(self, wid, move_action, build_action):
        move_from_xy = move_action['xy1']
        move_to_xy = move_action['xy2']

        build_from_xy = build_action['xy1']
        build_to_xy = build_action['xy2']

        move_direction = self.__get_direction(move_from_xy, move_to_xy)
        build_direction = self.__get_direction(build_from_xy, build_to_xy)
        self.write_to_output([wid, *move_direction, *build_direction])


    def give_up(self, pid):
        self.write_to_output("Player gave up: {}.".format(pid))
      
    def error(self, pid, message):
        self.write_to_output("Player error by: {}. {}".format(pid, message.value))


    def game_over(self, pid, wid, move_action):
        move_from_xy = move_action['xy1']
        move_to_xy = move_action['xy2']

        move_direction = self.__get_direction(move_from_xy, move_to_xy)
        self.write_to_output([wid, *move_direction])
        self.write_to_output('"' + str(pid) + '"')

    def write_to_output(self, message):
        self.output.write(str(message) + "\n")


    def __get_direction(self, from_xy, to_xy):
        from_x, from_y = from_xy
        to_x, to_y = to_xy
    
        return [self.__east_west(from_x, to_x), self.__north_south(from_y, to_y)]

    
    def __north_south(self, from_y, to_y):
        if to_y is from_y:
            return "PUT"
        elif to_y > from_y:
            return "SOUTH"
        else:
            return "NORTH"

    def __east_west(self, from_x, to_x):
        if to_x is from_x:
            return "PUT"
        elif to_x > to_x:
            return "EAST"
        else:
            return "WEST"

    
    def __cell(self, height, player_id, worker_id):
        if player_id is None:
            return height
        return "{}{}{}".format(height, player_id, worker_id)


if __name__ == "__main__":
    player_1 = MisbehavingPlayer("one")
    player_2 = Player("two")

    Referee(player_1, player_2, time_limit=1, observers=[XObserver()]).run_games()
