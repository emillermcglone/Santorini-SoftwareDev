import timeout_decorator
from timeout_decorator.timeout_decorator import TimeoutError
import json

@timeout_decorator.timeout(5)
def get_json_input():
    return input()

def get_json_inputs():
    """ 
    Listen for JSON inputs
    Note: time out after 5 seconds
    """

    current_input = ""
    json_inputs = []

    while True:
        try: 
            json_input = get_json_input()
            current_input += json_input
            json.loads(current_input)
            json_inputs.append(current_input)
            current_input = ""
        except EOFError:
            break
        except TimeoutError:
            current_input = ""
            print("Timeout: insert another JSON value")
            continue
        except json.JSONDecodeError:
            continue

    return json_inputs

def concatenate_json_inputs(inputs):
    """ Concatenate reverse positions of inputs """

    length = len(inputs)
    result = []

    for input in inputs:
        result.append("[%d, %s]" % (length - 1, input))
        length -= 1
    
    return result

def echo_json_inputs():
    for input in concatenate_json_inputs(get_json_inputs()):
        print(input)

if __name__ == "__main__":
    echo_json_inputs()