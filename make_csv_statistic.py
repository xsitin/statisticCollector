import asyncio
from time import gmtime, strftime


def make_statistic(groups: dict):
    table_name = strftime("%Y-%m-%d %H-%M-%S", gmtime()) + '.csv'
    companies = list(groups.keys())
    companies.sort(key=lambda x: len(groups[x]), reverse=True)
    with open(table_name, 'w', encoding="utf8") as table:
        table.write('Название компании,Кол-во сотрудников\n')
        for company in companies:
            table.write(f'{company},{len(groups[company])}\n')
    print(f"View statistic in {table_name}")
