from hak.one.string.print_and_return_false import f as pf
from hak.one.dict.financial_year.make import f as mkfy

# to_str
f = lambda x: f"{x['start_year']} - {x['final_year']}"

def t():
  x = mkfy({'start_year': 2022})
  y = '2022 - 2023'
  z = f(x)
  return y == z or pf([f'x: {x}', f'y: {y}', f'z: {z}'])
