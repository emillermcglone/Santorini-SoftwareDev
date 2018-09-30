from splitstream import splitfile

import json
import fileinput

with fileinput.input() as f:
    for line in splitfile(f, format="json"):
        print(line)