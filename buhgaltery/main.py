import datetime as dt
from application import salary
from application.db import people


print(f'Сейчас:\n'
     f'{dt.datetime.today()}\n\n')

if __name__ == '__main__':
    salary.salary()
    people.people()