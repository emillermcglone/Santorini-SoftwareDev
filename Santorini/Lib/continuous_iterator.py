class ContinuousIterator:
    """
    Iterable class that loops over list of players continuously. 
    """

    def __init__(self, items):
        """
        Initialize iterable with list of items to loop over. 

        :param items: [Any, ...], list of items to loop over
        """
        self.items = items
        self.index = 0
        self.end = len(items)


    def __iter__(self):
        return self


    def __next__(self):
        """ Iterate continuously """
        if self.end is 0:
            raise StopIteration

        if self.index is self.end:
            self.index = 0

        item = self.items[self.index]
        self.index += 1
        return item