import asyncio
import configparser
import math

from vkwave_api import API

from user import User

config = configparser.ConfigParser()
config.read("settings.ini")
service_key = config['vk']['token']
group_id = "427003"


async def getUsers():
    ids = []
    users = []
    api = API(service_key)
    vk = api.get_api()
    members_count = (await vk.groups.get_by_id(group_id=group_id, fields="members_count")).response.pop().dict()[
        "members_count"]
    requests = []

    for i in range(math.ceil(members_count / 1000)):
        ids.extend((await vk.groups.get_members(group_id=group_id, offset=i * 1000, count=1000)).response.items)
    for id in ids:
        vk = api.get_api()
        request = vk.users.get(user_ids=id, fields="occupation")
        requests.append(asyncio.create_task(request))
    await asyncio.wait(requests)

    for answer in requests:
        answer = answer.result().response.pop().dict()
        if not answer["occupation"] is None \
                and answer["occupation"]['type'] == 'work' \
                and not answer["occupation"]['id'] is None:
            users.append(
                User(answer['id'], answer["occupation"]['id'],
                     answer["occupation"]['name']))
    await api.close()
    return users


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    task = loop.create_task(getUsers())
    loop.run_until_complete(task)
    print(task.result())
    print(len(task.result()))
