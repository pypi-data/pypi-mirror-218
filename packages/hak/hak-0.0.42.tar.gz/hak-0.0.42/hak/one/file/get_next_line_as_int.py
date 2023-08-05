from hak.one.file.save import f as save_file
from hak.one.file.remove import f as remove_file
from hak.one.string.print_and_return_false import f as pf

# get_next_line_as_int
f = lambda file: int(file.readline()[:-1])

def up():
  x = {'filename': './foo.txt', 'count': 10}
  x['content'] = save_file(
    x['filename'],
    '\n'.join([str(_) for _ in range(x['count'])]) + '\n'
  )
  return x

dn = lambda x: remove_file(x['filename'])

def t():
  x = up()
  y = [_ for _ in range(x['count'])]
  with open(x['filename'], 'r') as file:
    z = [f(file) for _ in range(x['count'])]
  dn(x)
  return y == z or pf([f'x: {x}', f'y: {y}', f'z: {z}'])
