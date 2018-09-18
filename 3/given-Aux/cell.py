from enum import Enum


class Cell(object):
    class CellContents(Enum):
        """
        The types of items within a cell
        """
        Empty = 0
        Formula = list
        Constant = int
        Reference = tuple

        @staticmethod
        def is_valid_cell(obj):
            """
            Checks to see if the given obj is a cell
            :param obj:
            :return:
            """
            return type(obj) is Cell.CellContents.Empty.value \
                   or type(obj) is Cell.CellContents.Formula.value \
                   or type(obj) is Cell.CellContents.Reference.value \
                   or type(obj) is Cell.CellContents.Constant.value

    def __init__(self, contents):
        """
        Initializes a Cell with the given contents
        :param contents: The contents to init the cell with
        """
        if type(contents) is Cell:
            contents = contents.contents
        if not Cell.CellContents.is_valid_cell(contents):
            print("Invalid Contents")
            raise ValueError
        self.contents = contents

    def evaluate_contents(self, cells):
        """
        Evaluate the contents of the cell
        :param cells: The cells of the spreadsheet to reference
        :return: The value of the cell (int)
        """
        if type(self.contents) is Cell.CellContents.Formula.value:
            return self.resolve_and_evaluate(cells)
        elif type(self.contents) is Cell.CellContents.Empty.value:
            return Cell.CellContents.Empty
        elif type(self.contents) is Cell.CellContents.Constant.value:
            return self.contents
        elif type(self.contents) is Cell.CellContents.Reference.value:
            return Cell(cells[tuple(self.contents)]).evaluate_contents(cells)

    def resolve_and_evaluate(self, cells):
        """
        Flattens out the cell and performs operations
        :param cells: The cells of the spreadsheet to reference
        :return: The value of the cell (int)
        """
        formula = self.contents
        operators = ["+", "*"]
        resolved_formula = []
        for clause in formula:
            if clause not in operators:
                value = Cell(clause).evaluate_contents(cells)
                resolved_formula.append(value)
            else:
                resolved_formula.append(clause)
        return self.evaluate_formula(operators, resolved_formula)

    def get_references(self):
        """
        Retrieves the references within the cell to other cells
        :return: []
        """
        references = []
        if type(self.contents) is Cell.CellContents.Formula.value:
            references.extend(self.get_references_helper())
        elif type(self.contents) is Cell.CellContents.Reference.value:
            references.append(self.contents)
        return references

    def get_references_helper(self):
        """
        Helper function for get_references
        :return: []
        """
        for value in self.contents:
            return Cell(value).get_references()

    def evaluate_formula(self, operators, resolved_formula):
        """
        Performs operations
        :param operators: The operators to look for
        :param resolved_formula: The flattened formula
        :return: int
        """
        result = 0
        operator = "+"
        for ele in resolved_formula:
            if ele not in operators:
                if operator == "+":
                    result += ele
                elif operators == "*":
                    result *= ele
            else:
                operator = ele
        return result
