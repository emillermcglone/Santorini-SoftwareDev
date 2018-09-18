
class Formula(object):
    def __init__(self, formula):
        """
        Can't have this just be a string as a formula is one of multiple types.
        To try and parse it all from a string isn't efficient and cumbersome
        In fact, using a string at all to represent the formulas isn't helpful
        set self.formula to the input value. update type if its digit or formula
        :param formula: input formula
        """
        self.formula = formula

    def evaluate(self, sheet):
        """
        evaluate formula using input dict? what's the point of the dict?
        shouldn't the formula/spreadsheet classes contain all req'd info?
        does it work like the spreadsheet stores no useful data, just references
        to arbitrary cells, and the dict says what this reference represents?
        Got rid of the given mapping dictionary, it's unnecessary. Instead just giving
        function the formula in the spreadsheet
        :returns: output value from evaluation
        """
        if type(self.formula) is int:
            return self.formula
        elif type(self.formula) is list:
            resolved_formula = self.resolve_formula(sheet)
            operators = ["+", "*"]
            current_operator = "+"
            result = 0
            for ele in resolved_formula:
                if ele in operators:
                    current_operator = ele
                else:
                    if current_operator is "+":
                        result += ele
                    else:
                        result *= ele
            return result
        elif type(self.formula) is tuple:
            return sheet[self.formula[0]][self.formula[1]].evaluate(sheet)
        elif type(self.formula) is Formula:
            return self.formula.formula.evaluate(sheet)

    def resolve_formula(self, sheet):
        formula_copy = self.formula
        for i in range(0, len(formula_copy)):
            if type(formula_copy[i]) is list:
                formula_copy[i] = Formula(formula_copy[i]).evaluate(sheet)
            elif type(self.formula[i]) is tuple:
                tup = tuple(self.formula[i])
                self.formula[i] = sheet[tup[0]][tup[1]].evaluate(sheet)
            elif type(self.formula[i]) is Formula:
                self.formula[i] = self.formula[i].evaluate(sheet)
        return formula_copy

    def get_references(self):
        references = []
        if type(self.formula) is list:
            references.extend(self.get_references_helper())
        elif type(self.formula) is tuple:
            references.append(self.formula)
        elif type(self.formula) is Formula:
            references.append(self.formula.formula.get_references())
        return references

    def get_references_helper(self):
        for value in self.formula:
            return Formula(value).get_references()


class Spreadsheet(object):
    sheet = [[]]

    def __init__(self, rectangle):
        """
        initialize self.sheet using values form rectangle argument
        :param rectangle: nested 2d array of formulae, expected format: [[]]
        """
        self.sheet = rectangle
        width = len(rectangle[0])
        for i in range(0, len(rectangle)):
            if width != len(rectangle[i]):
                print("Invalid Rectangle")
            for j in range(0, len(rectangle[i])):
                    self.check_references(i, j, rectangle[i][j])

    def get_value(self, x: int, y: int):
        """
        fetch value from self.sheet located at input x,y coordinates
        
        :param x: x coordinate
        :param y: y coordinate
        :return: value of cell @ x,y
        :raises IndexError: if indices are invalid
        """
        try:
            targetFormula = self.sheet[x][y]
            return targetFormula.evaluate(self.sheet)
        except:
            raise IndexError

    def update(self, x: int, y: int, formula):
        """
        set formula @ cell x,y with input value
        :param x: x coodinate
        :param y: y coordinate
        :param formula: input formula to insert to self.sheet
        """
        try:
            self.check_references(x, y, formula)
            try:
                self.sheet[x][y] = formula
            except IndexError:
                print("Invalid Indices")
        except ValueError:
            print("Circular Reference")

    def check_references(self, x, y, formula):
        """
        Checks for circular references
        :param x: The x coord of cell that the formula is located at
        :param y: The y coord of cell that the formula is located at
        :param formula: The formula containing potential references
        :return: None
        :exception Value Error
        """
        if type(formula.formula) is list:
            self.check_references_helper(x, y, formula.formula)
        elif type(formula.formula) is tuple:
            self.check_reference(x, y, formula.formula)
        elif type(formula.formula) is Formula:
            self.check_references(x, y, formula.formula)

    def check_references_helper(self, x, y, formula_contents):
        """
        Helper for check_references
        :param x: The x coord of cell that the formula is located at
        :param y: The y coord of cell that the formula is located at
        :param formula: The formula containing potential references
        :return: None
        :exception Value Error
        """
        for ele in formula_contents:
            if type(ele) is tuple:
                self.check_reference(x, y, ele)
            elif type(ele) is Formula:
                self.check_references(x, y, ele)

    def check_reference(self, x, y, tup):
        """
        Checks if the given tuple is circular
        :param x: The x coord of cell that the formula is located at
        :param y: The y coord of cell that the formula is located at
        :param tup: The tuple containing potential references
        :return: None
        :exception Value Error
        """
        tup = tuple(tup)
        if tup == (x, y):
            raise ValueError
        references = self.sheet[x][y].get_references()
        for reference in references:
            if (x, y) in self.sheet[reference[0]][reference[1]].get_references():
                print("Circular Reference")
