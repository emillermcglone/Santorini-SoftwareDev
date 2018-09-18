import json
from splitstream import splitfile
import fileinput
import sys
import io

def generate_json(file_name):
    for line in splitfile(file_name, format="json"):
        print(json.loads(line))

generate_json(io.BytesIO('[1, 2]asdfdfa[3, 4]fdafdf[123, 4231]{"a": 23}'.encode())) 