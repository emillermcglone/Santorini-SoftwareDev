import re
import csv
from ast import literal_eval as make_tuple

class Spreadsheet:
    def __init__(self):
        self.__table = {}

    def create_spreadsheet(self, path):
        """ 
        Create coordinates and formulae mapping from csv that has only two columns
        separated by semi-colons instead of commas. First contains coordinates as 
        tuples and the second valid formulae. Any invalid values are skipped.
        """
        with open(path, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            for row in reader:
                try:
                    self.__table[make_tuple(row[0])] = row[1]
                except:
                    continue

    def get_value(self, cell):
        """ Get value of cell. Otherwise, return None """
        if cell in self.__table:
            return self.__evaluate(self.__table[cell])
        else:
            return None

    def put_value(self, cell, value):
        """ Update cell with formula """
        if cell in self.__table:
            self.__table[cell] = value

    def __evaluate(self, value):
        """ Evaluate a formula's value """
        formula = value
        tuple_mappings = self.__extract_refs(value)
        for key, value in tuple_mappings:
            formula = formula.replace(key, str(self.__evaluate(value)))
        return eval(formula, {'__builtins__': {}})

    def __extract_refs(self, value):
        """ Extract cell references from value """
        tuple_format = r"\([-+]?\d+\,\s*[-+]?\d+\)"
        tuples = re.findall(tuple_format, value)
        return list(map(lambda tuple: (tuple, self.__table[make_tuple(tuple)]), tuples))