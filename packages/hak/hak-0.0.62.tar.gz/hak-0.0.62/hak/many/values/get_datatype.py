from hak.one.dict.rate.make import f as make_rate
from hak.one.string.print_and_return_false import f as pf
from hak.pxyz import f as pxyz

# detect_datatype_from_values
def f(values):
  _types = set([type(_) for _ in values])
  if type(None) in _types: _types.remove(type(None))
  # if len(_types) > 1: return 'mixed'
  
  _type = _types.pop()
  if   _type == type('abc'): return 'str'
  elif _type == type(1): return 'int'
  elif _type == type(1.0): return 'float'
  elif _type == type(True): return 'bool'
  elif _type == type(1j): return 'complex'
  elif _type == type(make_rate(1,1)): return 'rate'
  else: raise NotImplementedError('Code not written for this type yet.')

def t_0():
  x = ['abc', 'xyz', None]
  y = 'str'
  z = f(x)
  return pxyz(x, y, z)

def t_1():
  x = [1, 2, None]
  y = 'int'
  z = f(x)
  return pxyz(x, y, z)

def t_2():
  x = [1.1, 2.2, None]
  y = 'float'
  z = f(x)
  return pxyz(x, y, z)

def t_3():
  x = [True, False, None]
  y = 'bool'
  z = f(x)
  return pxyz(x, y, z)

def t_4():
  x = [0+1j, 1+0j, None]
  y = 'complex'
  z = f(x)
  return pxyz(x, y, z)

def t_5():
  x = [make_rate(110, 72), make_rate(72, 111), None]
  y = 'rate'
  z = f(x)
  return pxyz(x, y, z)

def t():
  if not t_0(): return pf('t_0 failed')
  if not t_1(): return pf('t_1 failed')
  if not t_2(): return pf('t_2 failed')
  if not t_3(): return pf('t_3 failed')
  if not t_4(): return pf('t_4 failed')
  if not t_5(): return pf('t_5 failed')
  return True
