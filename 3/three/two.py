#!/usr/bin/env python3.6

import timeout_decorator
from timeout_decorator.timeout_decorator import TimeoutError
import sys, json, fileinput

def is_json(value):
    """ Is given value a valid JSON value? """
    try:
        json.loads(value)
        return True
    except:
        return False

def parse_input_into_jsons(previous_input, value):
    """ Splits JSON values from value and return leftover """
    new_value = previous_input
    json_list = []

    for c in value:
        new_value += c
        if is_json(new_value):
            json_list.append(new_value)
            new_value = ""
    
    return (json_list, new_value)

def get_json_inputs(inputs):
    """ 
    Filters input source for valid JSON values 
    Closes source when Enter or ^D are detected, or after 10 second timeout
    """

    compiled_input = ""
    get_json_input = timeout_decorator.timeout(10)(inputs.readline)
    json_inputs = []

    while True:
        try:
            current_input = get_json_input().rstrip('\n')
            (parsed_jsons, leftover) = parse_input_into_jsons(compiled_input, current_input)
            json_inputs += parsed_jsons
            compiled_input = leftover
        except (TimeoutError, KeyboardInterrupt):
            print("Terminated")
            break

        if current_input == "^D" or current_input == "": 
            break

        if is_json(compiled_input):
            json_inputs.append(compiled_input)
            compiled_input = ""

    inputs.close()
    return json_inputs

def concatenate_json_inputs(inputs):
    """ Concatenate reverse positions to inputs """
    if inputs is None: return []
    return list(zip(reversed(range(len(inputs))), inputs))

def format_json_inputs(inputs):
    result = ""
    for position, json_input in concatenate_json_inputs(get_json_inputs(inputs)):
        result += "[%d, %s]\n" % (position, json_input)

    return result

def echo_json_inputs(inputs, output):
    """ Echo JSON inputs to command line """
    for i in format_json_inputs(inputs):
        output.write(i)

if __name__ == "__main__":
    echo_json_inputs(fileinput.input(), sys.stdout)