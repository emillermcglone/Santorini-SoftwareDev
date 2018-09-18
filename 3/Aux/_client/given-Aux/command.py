from enum import Enum

from spreadsheet import Spreadsheet

class Command(object):
    """
    Used to encapsulate command information and simplify command functionality
    """
    class CommandEnum(Enum):
        """
        Enum for types of commands
        """
        SHEET = "SHEET"
        SET = "SET"
        AT = "AT"

    def __init__(self, command):
        """
        Initialize the command class with the given command type and spreadsheet name as well as command
        :param command: The command to create
        """
        self.command_type = command[0].upper()
        self.spreadsheet_name = command[1].upper()
        self.command = command

    def execute(self, spreadsheets):
        """
        Execute the command
        :param spreadsheets: The different spreadsheets to execute on
        :return:
        """
        if self.command_type == Command.CommandEnum.SHEET.value:
            cells = self.convert_to_form(list(self.command[2]))
            spreadsheets[self.spreadsheet_name] = Spreadsheet(cells=cells)
        elif self.command_type == Command.CommandEnum.SET.value:
            self.check_exist_spreadsheet(spreadsheets)
            x = int(self.command[2])
            y = int(self.command[3])
            formula = self.command[4]
            if type(formula) is list:
                formula = self.convert_to_form([formula])
            spreadsheets[self.spreadsheet_name].update_cell(x, y, formula)
        elif self.command_type == Command.CommandEnum.AT.value:
            self.check_exist_spreadsheet(spreadsheets)
            x = int(self.command[2])
            y = int(self.command[3])
            value = spreadsheets[self.spreadsheet_name].get_cell(x, y)
            if value:
                print(value)
        else:
            print("Invalid Command")
            raise ValueError

    def convert_to_form(self, rows):
        """
        Convert input to a format that can be used in program's objects
        :param rows: The rows to format
        :return: Formatted Rows []
        """
        for i in range(0, len(rows)):
            for j in range(0, len(rows[i])):
                if type(rows[i][j]) is list:
                    self.convert_helper(rows, i, j)
        return rows

    def convert_helper(self, rows, i, j):
        """
        Helper function for convert to form
        :param rows: The rows to format
        :param i: The index of the cell in the row to format (so that cell can be altered by reference)
        :param j: The index of the cell in the row to format (so that cell can be altered by reference)
        :return: None
        """
        if rows[i][j][0] == ">":
            rows[i][j] = (rows[i][j][1], rows[i][j][2])
        for k in range(0, len(rows[i][j])):
            if type(rows[i][j][k]) is list:
                self.convert_helper(rows[i], j, k)

    def check_exist_spreadsheet(self, spreadsheets):
        """
        Check if spreadsheet exists
        :param spreadsheets:
        :return:
        """
        if self.spreadsheet_name not in spreadsheets.keys():
            print("Spreadsheet Doesn't Exist")
            raise ValueError
