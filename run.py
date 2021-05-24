import sys

import asyncio
from make_csv_statistic import make_statistic
from get_users import VKGroupUsersCollector
import Visualization


def print_help():
    print("This program analyze members of vk group and represent the chart of their work places\n")
    print("Usage: python run.py group_id [service_key]")
    print("\tgroup_id - the id of vk group to analyze")
    print("\tservice_key - service key for vk api, if not presented will be taken from settings.ini")
    exit()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_help()
    if len(sys.argv) == 2:
        if sys.argv[1] == "/?" or sys.argv[1] == "--help" or sys.argv[1] == "-h":
            print_help()
        collector = VKGroupUsersCollector(sys.argv[1])
    else:
        collector = VKGroupUsersCollector(sys.argv[1], sys.argv[2])
    loop = asyncio.get_event_loop()
    get_groups_task = loop.create_task(collector.get_companies_with_users())
    get_group_name_task = loop.create_task(collector.get_group_name())
    loop.run_until_complete(get_groups_task)
    loop.run_until_complete(get_group_name_task)
    data = get_groups_task.result()
    make_statistic(data)
    Visualization.Visualize(data, get_group_name_task.result())
