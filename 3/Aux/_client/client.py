import sys
import fileinput
import json
import io

from splitstream import splitfile
from spreadsheet import Spreadsheet, Formula
from oslash import Just, Maybe, Nothing

sys.path.append('../2/Aux')
two = __import__('2')

spreadsheets = {}

def parse_json_formula(jf):
    """ Get the formula from the JSON format """
    json_value = json.loads(jf)
    if isinstance(json_value, int) and json_value >= 0:
        return str(json_value)
    elif isinstance(json_value, list) and json_value[0] == ">":
        return str((json_value[1], json_value[2]))
    else:
        v1, v2 = parse_json_formula(json_value[0]), parse_json_formula(json_value[2])
        return "(" + v1 + json_value[1] + v2 + ")"


def create_formula(jf):
    return Formula(parse_json_formula(str(jf)))


def at_request(req, output):
    """ Get value of cell in an existing spreadsheet """
    spreadsheet = spreadsheets[req[1]]
    value = spreadsheet.get_value(req[2], req[3])
    message = 'false' if value is None else value
    output.write(message)


def set_request(req, output):
    """ Set cell in an existing spreadsheet with new formula """
    if req[1] not in spreadsheets:
        return
    spreadsheet = spreadsheets[req[1]]
    spreadsheet.update(req[2], req[3], create_formula(req[4]))


def create_request(req, output):
    """ Create a new spreadsheet initialized with name and rectangle of formulae """
    if req[1] in spreadsheets:
        return
    new_rectangle = [list(map(lambda jf: create_formula(jf), l)) for l in req[2]]
    spreadsheet = Spreadsheet(new_rectangle)
    spreadsheets[req[1]] = spreadsheet


def handle_requests(source, output):
    """ Delegate every request to appropriate handlers """

    request_handlers = {
        "at": at_request, 
        "sheet": create_request,
        "set": set_request
    }

    for j in splitfile(source, format='json'):
        try:
            json_val = json.loads(j)
            request_handlers[json_val](json_val, output)
        except:
            continue            

if __name__ == "__main__":
    for line in fileinput.input():
        handle_requests(io.BytesIO(line.encode()), sys.stdout)
