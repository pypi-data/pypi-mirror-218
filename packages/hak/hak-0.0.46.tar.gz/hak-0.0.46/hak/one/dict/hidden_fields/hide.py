from hak.one.string.print_and_return_false import f as pf

f = lambda x: [k for k in x['field_names'] if k not in set(x['hidden_fields'])]

def t():
  x = {
    'hidden_fields': ['a', 'c', 'e'],
    'field_names': ['a', 'b', 'c', 'd', 'e']
  }
  y = ['b', 'd']
  z = f(x)
  return y == z or pf([f"x: {x}", f'y: {y}', f'z: {z}'])
