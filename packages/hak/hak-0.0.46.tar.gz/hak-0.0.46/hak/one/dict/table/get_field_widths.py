from copy import deepcopy
from hak.one.string.print_and_return_false import f as pf
from hak.one.dict.cell.get_width import f as get_width

def f(x):
  field_names = deepcopy(x['field_names'])
  records = x['records']
  return {
    field_name: max([
      get_width(
        {
          'value': record[field_name] if field_name in record else None,
          'field_name': field_name
        }
      )
      for record in records
    ])
    for field_name in field_names
  }

def t():
  x = {
    'field_names': ['a', 'b', 'c', 'd', 'e'],
    'records': [
      {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4},
      {'a': 5, 'b': 6, 'c': 7, 'd': 8, 'e': 9},
      {'a': 10, 'b': 11, 'c': 12, 'd': 13, 'e': 14},
    ]
  }
  y = {'a': 2, 'b': 2, 'c': 2, 'd': 2, 'e': 2}
  z = f(x)
  return y == z or pf([f"x: {x}", f'y: {y}', f'z: {z}'])
