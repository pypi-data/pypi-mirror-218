from datetime import date
from hak.one.string.print_and_return_false import f as pf
from hak.one.dict.financial_year.make import f as mkfy

# get_ω_date
f = lambda x: date(x['final_year'], 6, 30)

def t():
  x = mkfy({'start_year': 2022})
  y = date(2023, 6, 30)
  z = f(x)
  return y == z or pf([f'x: {x}', f'y: {y}', f'z: {z}'])
