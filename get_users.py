import asyncio
import configparser
import math
import re

from vkwave_api import API

from user import User
from company import Company

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
                and answer["occupation"]['type'] == 'work':
            if not answer["occupation"]['id'] is None:
                users.append(
                    User(answer['id'], answer["occupation"]['id'],
                     answer["occupation"]['name'], True))
            else:
                users.append(
                    User(answer['id'], None,
                         answer["occupation"]['name'], False))
    await api.close()
    return users


filter_words = ['ооо', "гк", "оао", "оа", "зао", "пф", "ао", "окб"]

translit = { 'a': 'а', 'b': 'б', 'c': 'ч', 'd': 'д', 'e': 'е', 'f': 'ф', 'g': 'г', 'h': 'х', 'i': 'и',
             'j': 'й', 'k': 'к', 'l': 'л', 'm': 'м', 'n': 'н', 'o': 'о', 'p': 'п', 'q': 'ю', 'r': 'р',
             's': 'с', 't': 'е', 'u': 'у', 'v': 'в', 'w': 'ш', 'x': 'щ', 'y': 'я', 'z': 'з'}


def normalize_name(name: str):
        name = name.lower()
        for filter_word in filter_words:
            name = re.sub(r"^|\W" + filter_word + r"\W", " ", name)
        new_name = ""
        for c in name:
            if c in translit:
                new_name += translit[c]
            elif c.isalpha():
                new_name += c
        return new_name


async def get_biggest_group(group_ids, vk):
    biggest_group = ''
    biggest_count = -1
    for id in group_ids:
        count = (await vk.groups.get_by_id(group_id=id, fields="members_count")).response.pop().dict()["members_count"]
        if count is not None and count > biggest_count:
            biggest_count = count
            biggest_group = id
    return biggest_group


async def group_users(users):
    jobs = {}
    api = API(service_key)
    vk = api.get_api()
    for user in users:
        job = normalize_name(user.group_name)
        if job in jobs:
            jobs[job].append(user)
        else:
            jobs[job] = [user]
    result = {}
    for job in jobs:
        groups = {}
        for user in jobs[job]:
            if user.is_group_id_defined:
                groups[user.group_id] = user.group_name
        if len(groups) == 0:
            company = Company(jobs[job][0].group_name, None)
        else:
            group_id = await get_biggest_group(groups, vk)
            if group_id in groups:
                company = Company(groups[group_id], group_id)
            else:
                continue
        result[company] = jobs[job]
    await api.close()
    return result


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    task = loop.create_task(getUsers())
    loop.run_until_complete(task)
    users = task.result()

    loop = asyncio.get_event_loop()
    task = loop.create_task(group_users(users))
    loop.run_until_complete(task)
    groups = task.result()
    for group in groups:
        print(group.company_name, end=" : ")
        print(len(groups[group]))
    #print(task.result())
    #print(len(task.result()))

