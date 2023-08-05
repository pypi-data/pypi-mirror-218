from hak.one.string.print_and_return_false import f as pf

# make_bar
f = lambda x: (
  "|-"+'-|-'.join(['-'*x['field_widths'][k] for k in x['field_names']])+"-|"
)

def t():
  x = {
    'field_widths': {'a': 2, 'b': 2, 'c': 2, 'd': 2, 'e': 2},
    'field_names': ['a', 'b', 'c', 'd', 'e'],
  }
  y = '|----|----|----|----|----|'
  z = f(x)
  return y == z or pf([f"x: {x}", f'y: {y}', f'z: {z}'])
