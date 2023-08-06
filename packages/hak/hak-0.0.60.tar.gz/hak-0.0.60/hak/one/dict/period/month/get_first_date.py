from datetime import date
from hak.one.string.print_and_return_false import f as pf

# get_first_date_of_month
f = lambda x: date(year=x['year'], month=x['month_number'], day=1)

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
  return True
