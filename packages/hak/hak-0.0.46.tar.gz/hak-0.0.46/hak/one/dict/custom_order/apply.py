from copy import deepcopy
from hak.one.string.print_and_return_false import f as pf

# apply_custom_order
def f(x):
  field_order = deepcopy(x['field_order'])
  field_names = deepcopy(x['field_names'])
  for field_name in field_order:
    if field_name in field_names:
      field_names.remove(field_name)
  return field_order + field_names

def t():
  x = {
    'field_order': ['c', 'b', 'a'],
    'field_names': ['a', 'b', 'c', 'd', 'e', 'f'],
  }
  y = ['c', 'b', 'a', 'd', 'e', 'f']
  z = f(x)
  return y == z or pf([f"x: {x}", f'y: {y}', f'z: {z}'])
