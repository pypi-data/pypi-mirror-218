from hak.one.string.print_and_return_false import f as pf
from hak.one.dict.financial_year.make import f as mkfy

# increment
f = lambda x: mkfy({'final_year': x['final_year']+1})

def t_a():
  x = mkfy({'start_year': 2022})
  y = mkfy({'start_year': 2023})
  z = f(x)
  return y == z or pf([f'x: {x}', f'y: {y}', f'z: {z}'])

def t():
  if not t_a(): return pf('!t_a')
  return True
