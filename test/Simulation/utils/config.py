'''
config.py

Functions for managing configuration files for a simulation.

TODO:
- fix relative paths
- add mutation functions
'''

import json

def load_json(p, format='json'):
  '''
  Load data from a file.

  args
    `f` (str): file to load

  kwargs
    `format` (str): file format
      - accepted formats: 'json'

  '''
  print('loading ', p)
  try:
    with open(p, 'r') as f:
      data = json.load(f)
      return data
  except FileNotFoundError:
    return False

def add_key(f, key, val):
  '''
  Adds
  '''
  pass
