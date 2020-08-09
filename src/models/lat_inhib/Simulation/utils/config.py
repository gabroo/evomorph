'''
config.py

Functions for managing configuration files for a simulation.

TODO:
- fix relative paths
- add mutation functions
'''

import json

def load_json(p):
  '''
  Load data from a file.

  args
    `f` (str): file to load

  '''
  try:
    with open(p, 'r') as f:
      data = json.load(f)
      return data
  except FileNotFoundError:
    return False

def write_json(d, p):
  '''
  Write data to a file.

  args
    `d` (dict, list): data to write

  '''
  try:
    with open(p, 'w') as f:
      json.dump(d, f)
      return True
  except Exception as e: 
      print(e)
      return False
