from hak.many.directories.empty.find import f as find_empty_directories
from hak.one.directory.remove import f as rmdir
from hak.one.string.print_and_return_false import f as pf
from hak.one.directory.make import f as mkdir

f = lambda root: set([rmdir(d) for d in find_empty_directories(root)])

def up():
  _root = './temp_root_A'
  _ = {'x': _root}
  _['temp_directories'] = [f'{_root}/temp_a', f'{_root}/temp_b']
  _['y'] = set([mkdir(x_i) for x_i in _['temp_directories']])
  _['created'] = _['y'] | set([_root])
  return _

def dn(x):
  for d in x['created']:
    rmdir(d)

def t():
  _up = up()
  x = _up['x']
  y = _up['y']
  z = f(x)
  dn(_up)
  return y == z or pf([f'x: {x}', f'y: {y}', f'z: {z}'])
