class Spreadsheet:
    def __init__(self, rectangle):
        pass

    def get_value(self, x, y):
        pass

    def update(self, x, y, formula):
        pass


class Formula:
    def __init__(self, string_formula):
        pass

    def get_references(self):
        """ Get all cell references in this formula"""
        pass

    def evaluate(self, dictionary):
        """ Evaluate formula with given mappings from references to values """
        pass
