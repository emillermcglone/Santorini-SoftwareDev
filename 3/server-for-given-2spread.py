import re, csv
from oslash import Maybe, Just, Nothing
from ast import literal_eval as make_tuple

class Spreadsheet:
    table = {}

    def __init__(self):
        self.table = {}

    def create_spreadsheet(self, path):
        """ Create coordinates and formulae mapping from csv """
        with open(path, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter = ';')
            for row in reader:
                print(row)
                try:
                    self.table[make_tuple(row[0])] = row[1]
                except:
                    continue

    def get_value(self, cell):
        """ Get value of cell """
        if cell in self.table:
            return Just(self.evaluate(self.table[cell]))
        else:
            return Nothing()

    def put_value(self, cell, value):
        """ Update cell with formula """
        if cell in self.table:
            self.table[cell] = value

    def evaluate(self, value):
        """ Evaluate a formula's value """
        formula = value
        tuple_mappings = self.extract_refs(value)
        for key, value in tuple_mappings:
            formula = formula.replace(key, str(self.evaluate(value)))
        return eval(formula, {'__builtins__':{}})
    
    def extract_refs(self, value):
        """ Extract cell references from value """
        tuple_format = r"\([-+]?\d+\,\s*[-+]?\d+\)"
        tuples = re.findall(tuple_format, value)
        return list(map(lambda tuple: (tuple, self.table[make_tuple(tuple)]), tuples))

spreadsheet = Spreadsheet()
spreadsheet.create_spreadsheet('sample-spreadsheet.csv')
print(spreadsheet.table)
print(spreadsheet.get_value((0, 0)))
spreadsheet.put_value((0,0), " 2 + 2")
print(spreadsheet.get_value((0, 0)))
print(spreadsheet.get_value((0, 1)))
print(spreadsheet.get_value((0, 2)))