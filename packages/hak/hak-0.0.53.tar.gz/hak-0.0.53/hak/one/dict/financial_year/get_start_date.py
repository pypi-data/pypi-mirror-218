from datetime import date
from hak.one.string.print_and_return_false import f as pf
from hak.one.dict.financial_year.make import f as mkfy

# get_α_date
f = lambda x: date(x['start_year'], 7, 1)

def t_a():
  x = mkfy({'start_year': 2022})
  y = date(2022, 7, 1)
  z = f(x)
  return y == z or pf([f'x: {x}', f'y: {y}', f'z: {z}'])

def t_b():
  x = mkfy({'final_year': 2022})
  y = date(2021, 7, 1)
  z = f(x)
  return y == z or pf([f'x: {x}', f'y: {y}', f'z: {z}'])

def t():
  if not t_a(): return pf('!t_a')
  if not t_b(): return pf('!t_b')
  return True
