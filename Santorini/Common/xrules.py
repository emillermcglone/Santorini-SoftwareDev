"""
Test harness for SantoriniRules
"""

import fileinput, io, sys, json, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from splitstream import splitfile


