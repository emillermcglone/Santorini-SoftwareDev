import json
from splitstream import splitfile
import fileinput
import sys

def generate_json(file_name):
    splitfile(file_name, format="json")

print(generate_json(sys.stdin))