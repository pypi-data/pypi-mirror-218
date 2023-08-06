from hak.one.string.print_and_return_false import f as pf

# src.string.year.is_a
# is_year
f = lambda x: len(x) == 4 and x.isdecimal()

def t():
  x = '2022'
  y = True
  z = f(x)
  return y == z or pf([f'x: {x}', f'y: {y}', f'z: {z}'])
