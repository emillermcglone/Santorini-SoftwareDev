import json as JSON
import sys
from command import Command


class CodemanistanExcel(object):
    def __init__(self):
        """
        Initializes and stores the spreadsheets in dict
        """
        self.spreadsheets = {}

    def run(self):
        """
        Runs the Codemanistan Excel Program
        :return:
        """
        try:
            for line in sys.stdin:
                try:
                    json = JSON.loads(line)
                    if type(json) == list and len(json) > 2:
                        try:
                            Command(json).execute(self.spreadsheets)
                        except ValueError:
                            pass
                    else:
                        print("Invalid Command")
                except ValueError:
                    print("Invalid JSON")
        except (KeyboardInterrupt, EOFError):
            exit(0)


if __name__ == '__main__':
    CodemanistanExcel().run()
