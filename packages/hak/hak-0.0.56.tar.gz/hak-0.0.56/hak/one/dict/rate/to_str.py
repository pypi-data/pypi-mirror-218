from hak.one.string.print_and_return_false import f as pf
from hak.one.dict.rate.make import f as make_rate
from hak.one.dict.rate.to_float import f as to_float

# __str__
f = lambda x: f"{to_float(x):.6f}"

def t():
  x = {'numerator': 710, 'denominator': 113}
  y = '6.283186'
  z = f(make_rate(x['numerator'], x['denominator']))
  return y == z or pf([f'x: {x}', f'y: {y}', f'z: {z}'])
