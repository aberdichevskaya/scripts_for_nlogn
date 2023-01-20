#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import json
import sys
import time
from requests.exceptions import HTTPError


# In[2]:


TOKEN = '4718f2553aa5bd49f68457e4d6a592f0285309d53e5dcc0b9456443abed77dd3c63fca16e1d0721029c2c8def8029c9c'
STARS_GROUPS = {192, 191, 286, 291, 297}


# In[3]:


def get_group_stars_id(groups):
    for group in groups:
        if (group['name'].find('звёзд') != -1 or group['name'].find('Stars') != -1) and group['id'] in STARS_GROUPS:
            return group['id']
    print('Группа звёздочек не найдена')
    group_id = int(input('Введите id группы звёздочек: '))
    if not group_id in STARS_GROUPS:
        print('Неверный id')
        sys.exit()
    return group_id


# In[4]:


def get_contests(contest_name):
    try:
        resp = requests.get('https://contest.nlogn.info/api/contest/all?token='+TOKEN, 
                              params={'count':3, 'query':contest_name})
        resp.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Error occurred: {err}')
    
    resp = resp.json()
    if len(resp['contests']) > 2 or len(resp['contests']) < 1:
        print('Неправильное название контеста')
        sys.exit()
      
    contest_id = resp['contests'][0]['id']
    group_ids = [group['id'] for group in resp['contests'][0]['allowedGroups']]
    contest_stars_id = -1
    groups_stars = []

    if len(resp['contests']) == 2:
        if resp['contests'][0]['name'] < resp['contests'][1]['name']:
            contest_stars_id = resp['contests'][1]['id']
            groups_stars = resp['contests'][1]['allowedGroups']
        else:
            contest_stars_id = contest_id
            groups_stars = resp['contests'][0]['allowedGroups']
            contest_id = resp['contests'][1]['id']
            group_ids = [group['id'] for group in resp['contests'][1]['allowedGroups']]
    else:
        # Название базового контеста и контеста со звёздочкой не совпадают
        print('Контест со звёздочкой не найден')
        contest_stars_name = input('Введите название контеста со звёздочкой: ')
        try:
            resp = requests.get('https://contest.nlogn.info/api/contest/all?token='+TOKEN, 
                              params={'count':3, 'query':contest_stars_name})
            resp.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Error occurred: {err}')
        resp = resp.json()
        if len(resp['contests']) > 1 or len(resp['contests']) < 1:
            print('Неправильное название контеста')
            sys.exit()
        contest_stars_id = resp['contests'][0]['id']
        groups_stars = resp['contests'][0]['allowedGroups']
                
    return contest_id, contest_stars_id, group_ids, get_group_stars_id(groups_stars)


# In[5]:


def join_contest(contest_id):
    try:
        resp = requests.get('https://contest.nlogn.info/api/contest/'+str(contest_id)+'/canJoin?token='+TOKEN)
        resp.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Error occurred: {err}')
    resp = resp.json()
    
    if resp['can'] == False:
        print('Нет доступа к контесту '+str(contest_id))
        sys.exit()
    if resp['joined'] == True:
        return
    
    try:
        resp = requests.post('https://contest.nlogn.info/api/contest/'+str(contest_id)+'/join?token='+TOKEN)
        resp.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Error occurred: {err}')


# In[8]:


def add_users_in_group(group_id, user_ids):
    try:
        resp = requests.get('https://contest.nlogn.info/api/admin/groups/'+str(group_id)+'?token='+TOKEN)
        resp.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Error occurred: {err}')
        
    group = resp.json()['group']   
    try:
        if group_id in STARS_GROUPS:
            requests.post('https://contest.nlogn.info/api/admin/groups/'+str(group_id)+'?token='+TOKEN,
                          data={'color':group['color'], 'groupId':str(group_id), 'name':group['name'], 'userIds': user_ids})
        else:
            print('Неправильный id группы звёздочек')
            sys.exit()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Error occurred: {err}')


# In[6]:


def check_contest_status(contest_id):
    try:
        resp = requests.get('https://contest.nlogn.info/api/admin/contests/'+str(contest_id)+'?token='+TOKEN)
        resp.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Error occurred: {err}')
        
    contest = resp.json()
    return contest['status'] != 'PRACTICE'


# In[7]:


def get_stars(contest_id, stars_set):
    try:
        resp = requests.get('https://contest.nlogn.info/api/contest/'+str(contest_id) + '?token='+TOKEN)
        resp = requests.get('https://contest.nlogn.info/api/contest/'+str(contest_id)+'/table2?token='+TOKEN, 
                              params={'contestId':contest_id, 'count':1000})
        resp.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Error occurred: {err}')
        
    resp = resp.json()
    tasks_number = len(resp['header'])
    stars = []
    for kid in resp['rows']:
        if kid['acceptedSolutionsInTime'] == tasks_number:
            stars.append(kid['user']['id'])
            if not kid['user']['id'] in stars_set:
                stars_set.add(kid['user']['id'])
                print(str(len(stars_set)) + '. ' + kid['user']['fullName'])
        else: 
            break
    
    return stars


# In[9]:


def add_groups_in_contest(contest_id, group_ids):
    try:
        resp = requests.get('https://contest.nlogn.info/api/admin/contests/'+str(contest_id)+'?token='+TOKEN)
        resp.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Error occurred: {err}')
        
    contest = resp.json()    
    problem_ids = []
    for problem in contest['problems']:
        problem_ids.append(problem['id']) 
    
    try:
        resp = requests.post('https://contest.nlogn.info/api/admin/contests/'+str(contest_id)+'?token='+TOKEN, 
                             data={'contestId': str(contest_id), 'durationTimeMs': contest['durationTimeMs'],
                                   'groupIds': group_ids, 'name': contest['name'],
                                   'practiceDurationTimeMs': contest['practiceDurationTimeMs'],
                                   'problemIds': problem_ids, 'relativeFreezeTimeMs': contest['relativeFreezeTimeMs'],
                                   'startTimeMs': contest['startTimeMs']})
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Error occurred: {err}')


# In[ ]:


contest_name = input('Введите название базового контеста: ')
contest_id, contest_stars_id, group_ids, group_stars_id = get_contests(contest_name)
join_contest(contest_id)
join_contest(contest_stars_id)

if group_stars_id in STARS_GROUPS:
    add_users_in_group(group_stars_id, [])

stars_set = set()
prev_stars = []
while check_contest_status(contest_id):
    stars = get_stars(contest_id, stars_set)
    if stars != prev_stars:
        add_users_in_group(group_stars_id, stars)
    prev_stars = stars
    time.sleep(30)
print('Контест окончен')

add_groups_in_contest(contest_stars_id, group_ids)
print('Контест со звёздочкой открыт для всех')
if group_stars_id in STARS_GROUPS:
    add_users_in_group(group_stars_id, [])
    print('Группа звёздочек очищена')
else:
    print('Невозможно очистить группу звёздочек')

