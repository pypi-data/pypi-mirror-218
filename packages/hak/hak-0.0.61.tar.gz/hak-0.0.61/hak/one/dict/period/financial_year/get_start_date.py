from datetime import date

from hak.one.dict.period.financial_year.make import f as mkfy
from hak.one.string.print_and_return_false import f as pf
from hak.pxyz import f as pxyz

# get_α_date
f = lambda x: date(x['start_year'], 7, 1)

def t_a():
  x = mkfy({'start_year': 2022})
  y = date(2022, 7, 1)
  z = f(x)
  return pxyz(x, y, z)

def t_b():
  x = mkfy({'final_year': 2022})
  y = date(2021, 7, 1)
  z = f(x)
  return pxyz(x, y, z)

def t():
  if not t_a(): return pf('!t_a')
  if not t_b(): return pf('!t_b')
  return True
