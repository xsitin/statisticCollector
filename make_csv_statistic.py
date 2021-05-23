import asyncio
from time import gmtime, strftime
from get_users import getUsers
from collections import Counter


def make_statistic(users):
    group_names = map(lambda user: user.group_name.replace(',', ''), users)
    counter = Counter(group_names)
    table_name = strftime("%Y-%m-%d %H-%M-%S", gmtime()) + '.csv'

    with open(table_name, 'w', encoding="utf8") as table:
        table.write('Название компании,Кол-во сотрудников\n')
        for comp, count in counter.most_common():
            table.write(f'{comp},{count}\n')
    print(f"View statistic in {table_name}")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    task = loop.create_task(getUsers())
    loop.run_until_complete(task)
    make_statistic(task.result())
