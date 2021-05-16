import re
import asyncio
from time import gmtime, strftime
from get_users import getUsers
from collections import Counter

remove_re = re.compile('ЗАО |ООО |ОАО |ИП |"|\'|«|»|, ', re.IGNORECASE)

convert_dict = {
    "урфу": "Уральский федеральный университет",
    "сбер": "Сбер",
    "ржд": "Российские железные дороги",
    "яндекс": "Яндекс",
    "контур": "Контур",
    "тинькофф": "Тинькофф"
}


def make_statistic(users):
    group_names = map(lambda user: normalize_group_name(user.group_name), users)
    counter = Counter(group_names)
    table_name = strftime("%Y-%m-%d %H:%M:%S", gmtime()) + '.csv'

    with open(table_name, 'w') as table:
        table.write('Название компании,Кол-во сотрудников\n')
        for comp, count in counter.most_common():
            table.write(f'{comp},{count}\n')
    print(f"View statistic in {table_name}")


def normalize_group_name(name):
    name = re.sub(remove_re, '', name)
    l_name = name.lower()
    for k, v in convert_dict.items():
        if k in l_name:
            return v
    return name


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    task = loop.create_task(getUsers())
    loop.run_until_complete(task)
    make_statistic(task.result())
