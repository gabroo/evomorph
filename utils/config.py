'''
config.py

Functions for managing configuration files for a simulation.

TODO:
- fix relative paths
- add mutation functions
'''

import json

def load_json(file):
  '''
  Returns data encoded in `file` or False on exception. Assumes JSON format.
  '''
  try:
    with open(file, 'r') as f:
      data = json.load(f)
      return data
  except FileNotFoundError:
    return False
