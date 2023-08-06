from datetime import date
from datetime import datetime as dt
from hak.one.string.print_and_return_false import f as pf
from hak.one.dict.financial_year.get_end_date import f as get_ω_d
from hak.one.dict.financial_year.get_start_date import f as get_α_d
from hak.one.dict.financial_year.make import f as mkfy

# contains_date
f = lambda fy, δ: (
  get_α_d(fy) <= (δ.date() if isinstance(δ, dt) else δ) <= get_ω_d(fy)
)

def t_true():
  x = {'fy': mkfy({'start_year': 2022}),'δ': date(2022, 7, 5)}
  y = True
  z = f(**x)
  return y == z or pf([f'x: {x}', f'y: {y}', f'z: {z}'])

def t_false():
  x = {'fy': mkfy({'start_year': 2022}),'δ': date(2022, 6, 5)}
  y = False
  z = f(**x)
  return y == z or pf([f'x: {x}', f'y: {y}', f'z: {z}'])

def t():
  if not t_true(): return pf('!t_true()')
  if not t_false(): return pf('!t_false()')
  return True
