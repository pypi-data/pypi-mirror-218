from hak.many.dicts.get_all_keys import f as get_field_names
from hak.many.values.get_datatype import f as detect_datatype_from_values
from hak.one.string.print_and_return_false import f as pf

# src.table.fields.datatypes.get
def f(x):
  return {
    field_name: detect_datatype_from_values([
      record[field_name] if field_name in record else None
      for record in x
    ])
    for field_name in get_field_names(x)
  }

def t():
  x = [
    {'a': True, 'b': 'abc'},
    {'a': True, 'b': 'def'},
    {'a': False, 'b': 'ghi'},
  ]
  y = {'a': 'bool', 'b': 'str'}
  z = f(x)
  return y == z or pf([f"x: {x}", f'y: {y}', f'z: {z}'])
