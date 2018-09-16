import json
from splitstream import splitfile

def generate_json(file_name):
    splitfile(open(file_name), format="json", callback=lambda x: print(x))

generate_json('sample-input')