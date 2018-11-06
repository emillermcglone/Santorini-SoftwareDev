import json, fileinput, sys
sys.path.append('./Santorini/')
sys.path.append('./gija-emmi/Santorini/')
sys.path.append('../Santorini/')
from timeout_decorator import timeout, TimeoutError
import names

from Admin.configurations.stdin_configuration import STDINConfiguration
from Admin.tournament_manager import TournamentManager

if __name__ == "__main__":
    conf = STDINConfiguration()
    manager = TournamentManager(conf)
    print(manager.run_tournament())

