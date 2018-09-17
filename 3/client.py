import sys
import fileinput
import json

from spreadsheet import *
from oslash import Just, Maybe, Nothing
from splitstream import splitfile

spreadsheets = {}

def write_to_output(func, output):
    def go():
        return func()
    
    if

def parse_json_formula(jf):
    json_value = json.loads(jf)
    if isinstance(json_value, int) and json_value >= 0:
        return str(json_value)
    elif isinstance(json_value, list) and json_value[0] == ">":
        return str((json_value[1], json_value[2]))
    else:
        return "(" + parse_json_formula(json_value[0]) + json_value[1] + parse_json_formula(json_value[2]) + ")"


def at_request(req):
    spreadsheet = spreadsheets[req[1]]
    value = spreadsheet.get_value(req[2], req[3])


def set_request(req):
    spreadsheet = spreadsheets[req[1]]
    spreadsheet.update(req[2], req[3], Formula(parse_json_formula(req[4])))

def create_request(req):
    if req[2] in spreadsheets:
        return
    spreadsheet = Spreadsheet(req[2])
    spreadsheets[req[1]] = spreadsheet

def handle_request(req):
    request_type = req[0]
    if request_type == "sheet":
        create_request(request)
    elif request_type == "set":
        set_request(request)
    elif request_type == "at":
        at_request(request)
    else:
        pass


def pass_json_inputs(input_source):
    try:
        request = json.loads(input_source.readline())
    except:
        return
