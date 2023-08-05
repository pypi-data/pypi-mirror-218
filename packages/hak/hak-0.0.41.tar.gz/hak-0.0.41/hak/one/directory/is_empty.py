from hak.one.directory.filepaths.get import f as get_filepaths
from hak.one.string.print_and_return_false import f as pf
from hak.one.directory.make import f as mkdir
from hak.one.directory.remove import f as rmdir

f = lambda x: len(get_filepaths(root=x, filepaths=[])) <= 0

def t_false():
  x = './hak'
  y = False
  z = f(x)
  return y == z or pf([f'x: {x}', f'y: {y}', f'z: {z}'])

def up():
  x = './hak/directory/temp'
  mkdir(x)
  return x

dn = lambda x: rmdir(x)

def t_true():
  x = up()
  y = True
  z = f(x)
  dn(x)
  return y == z or pf([f'x: {x}', f'y: {y}', f'z: {z}'])

def t():
  if not t_false(): pf('!t_false')
  if not t_true(): pf('!t_true')
  return True
