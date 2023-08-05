from hak.many.directories.get import f as get_directories
from hak.one.directory.is_empty import f as is_empty
from hak.one.directory.make import f as mkdir
from hak.one.string.print_and_return_false import f as pf
from hak.one.directory.remove import f as rmdir

f = lambda root: set([d for d in get_directories(root) if is_empty(d)])

def up():
  _root = './temp_root_B'
  _ = {'x': _root}
  _['temp_directories'] = [f'{_root}/temp_a', f'{_root}/temp_b']
  _['created'] = set([mkdir(x_i) for x_i in _['temp_directories']])
  return _

def dn(created):
  for d in created:
    rmdir(d)

def t():
  _up = up()
  x = _up['x']
  y = _up['created']
  z = f(x)
  dn(_up['created'])
  return y == z or pf([f'x: {x}', f'y: {y}', f'z: {z}'])
