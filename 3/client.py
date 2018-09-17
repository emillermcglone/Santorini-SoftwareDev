import sys
import fileinput
import json

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

def at_request(req):
    pass

def set_request(req):
    pass

def create_request(req):

    pass

def pass_json_inputs(input_source):
    try:
        request = json.loads(input_source.readline())
        request_type = request[0]
    except: 
        pass

    if request_type == "sheet":
        create_request(request)
    elif request_type == "set":
        set_request(request)
    elif request_type == "at":
        at_request(request)
    else:
        pass


if __name__ == "__main__":
    main()
