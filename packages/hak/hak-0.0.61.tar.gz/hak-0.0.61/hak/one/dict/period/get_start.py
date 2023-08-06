from datetime import date

from hak.one.dict.period.financial_year.get_start_date import f as f_fy
from hak.one.dict.period.financial_year.make import f as mkfy
from hak.one.dict.period.month.get_start_date import f as f_m
from hak.one.string.print_and_return_false import f as pf
from hak.pxyz import f as pxyz

# get_α
f = lambda x: f_fy(x) if 'start_year' in x else f_m(x)

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

t_0 = lambda: date(2016,  5, 1) == f({'year': 2016, 'month_number':  5})
t_1 = lambda: date(2017,  6, 1) == f({'year': 2017, 'month_number':  6})
t_2 = lambda: date(2020,  2, 1) == f({'year': 2020, 'month_number':  2})
t_3 = lambda: date(2021,  2, 1) == f({'year': 2021, 'month_number':  2})
t_4 = lambda: date(2021, 12, 1) == f({'year': 2021, 'month_number': 12})

def t():
  if not t_0(): return pf('!t_0')
  if not t_1(): return pf('!t_1')
  if not t_2(): return pf('!t_2')
  if not t_3(): return pf('!t_3')
  if not t_4(): return pf('!t_4')
  if not t_a(): return pf('!t_a')
  if not t_b(): return pf('!t_b')
  return True
