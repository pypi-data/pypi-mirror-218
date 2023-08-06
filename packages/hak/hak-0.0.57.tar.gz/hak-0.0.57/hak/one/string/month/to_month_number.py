from hak.data.months import months
from hak.one.string.print_and_return_false import f as pf

# src.string.month.to_month_number
# to_month_number
def f(x):
  _x = x.lower()[:3]
  months_list = [m[:3].lower() for m in months]
  if _x in months_list: return months_list.index(_x) + 1
  return int(_x)

def t_0():
  x = 'January'
  y = 1
  z = f(x)
  return y == z or pf([f'x: {x}', f'y: {y}', f'z: {z}'])

def t_1():
  x = '12'
  y = 12
  z = f(x)
  return y == z or pf([f'x: {x}', f'y: {y}', f'z: {z}'])

def t():
  if not t_0(): return pf('t_0 failed')
  if not t_1(): return pf('t_1 failed')
  return True
