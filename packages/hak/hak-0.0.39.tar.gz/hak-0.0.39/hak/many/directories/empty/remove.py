from hak.many.directories.empty.find import f as find_empty_directories
from hak.one.directory.remove import f as rmdir
from hak.one.string.print_and_return_false import f as pf
from hak.one.directory.make import f as mkdir

f = lambda root: set([rmdir(d) for d in find_empty_directories(root)])

def up():
  _root = './temp_root'
  _ = {'x': _root}
  _['temp_directories'] = [f'{_root}/temp_a', f'{_root}/temp_b']
  _['created'] = set([mkdir(x_i) for x_i in _['temp_directories']])
  return _

def t():
  _up = up()
  x = _up['x']
  y = _up['created']
  z = f(x)
  return y == z or pf([f'x: {x}', f'y: {y}', f'z: {z}'])
