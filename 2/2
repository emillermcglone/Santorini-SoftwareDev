#!/usr/bin/env python3.6

from functools import wraps
import errno
import os
import signal
import sys, json, fileinput

class TimeoutError(Exception):
    pass

def timeout(seconds = 5, error_message = os.strerror(errno.ETIME)):
    """ Function wrapper for timing out """
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError(error_message)

        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result

        return wraps(func)(wrapper)

    return decorator

def is_json(value):
    """ Is given value a valid JSON value? """
    try:
        json.loads(value)
        return True
    except:
        return False

def get_json_inputs(inputs):
    """ 
    Filters input source for valid JSON values 
    Closes source when Enter or ^D are detected, or after 10 second timeout
    """

    compiled_input = ""
    get_json_input = timeout(10)(inputs.readline)
    json_inputs = []

    while True:
        try:
            current_input = get_json_input().rstrip('\n')
            compiled_input += current_input
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

def echo_json_inputs(inputs, output):
    """ Echo JSON inputs to command line """
    for position, json_input in concatenate_json_inputs(get_json_inputs(inputs)):
        output.write("[%d, %s]\n" % (position, json_input))

def main():
    echo_json_inputs(fileinput.input(), sys.stdout)

if __name__ == "__main__":
    main()