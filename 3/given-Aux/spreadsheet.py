from cell import Cell


class Spreadsheet(object):
    def __init__(self, width=10, height=10, cells=None):
        """
        Initializes Spreadsheet class
        :param width: Sets the width of spreadsheet (defaults to 100 cells)
        :param height: Sets the height of spreadsheet (defaults to 100 cells)
        :param cells: The given cells to build the spreadsheet from
        """
        self.cells = {}
        self.width = width
        self.height = height
        if cells:
            self.width = len(cells[0])
            self.height = len(cells)
        for i in range(0, self.height):
            if cells:
                if len(cells[i]) != self.width:
                    print("Invalid Rectangle")
                    raise ValueError
            for y in range(0, self.width):
                if not cells:
                    self.cells[(i, y)] = Cell(Cell.CellContents.Empty)
                else:
                    self.cells[(i, y)] = Cell(cells[i][y])

        for i in range(0, self.height):
            for y in range(0, self.width):
                    self.check_reference(i, y, cells[i][y])

    def get_cell(self, x: int, y: int):
        """
        Gets the cell at the given coords
        :param x: The x coord
        :param y: The y coord
        :return: The cell's value
        """
        if self.check_bounds(x, y):
            return self.cells[(x, y)].evaluate_contents(self.cells)
        else:
            print("Invalid Bounds")

    def update_cell(self, x: int, y: int, contents):
        """
        Updates the cell at the given coords with the given contents
        :param x: The x coord
        :param y: The y coord
        :param contents: The contents to use in cell
        :return: None
        """
        if self.check_bounds(x, y):
            self.check_reference(x, y, contents)
            self.cells[(x, y)] = Cell(contents)
        else:
            print("Invalid Bounds")

    def check_reference(self, x, y, contents):
        """
        Helper method to check if the given contents contains a circular reference somewhere
        :param x: The x coord of cell to check
        :param y: The y coord of cell to check
        :param contents: The contents of cell to check (look for other cells with other references)
        :return: None
        :exception Value Error
        """
        if type(contents) is Cell.CellContents.Reference.value:
            if self.check_bounds(contents[0], contents[1]):
                contents = tuple(contents)
                if contents == (x, y):
                    print("Circular Reference")
                    raise ValueError
                references = self.cells[(x, y)].get_references()
                for reference in references:
                    if (x,y) in self.cells[reference].get_references():
                        print("Circular Reference")
                        raise ValueError
            else:
                print("Invalid Reference")
                raise ValueError
        elif type(contents) is Cell.CellContents.Formula.value:
            self.check_reference_helper(x, y, contents)

    def check_reference_helper(self, x, y, contents):
        """
        Helper function for finding a circular reference
        :param x: The x coord of cell to check
        :param y: The y coord of cell to check
        :param contents: The contents of cell to check (look for other cells with other references)
        :return: None
        :exception Value Error
        """
        for ele in contents:
            self.check_reference(x, y, ele)

    def check_bounds(self, x, y):
        """
        Check the bounds of the given coords
        :param x: X coord to check
        :param y: Y coord to check
        :return: Boolean
        """
        return (self.width > x >= 0) and (self.height > y >= 0)
