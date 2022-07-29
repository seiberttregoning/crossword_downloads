#!/usr/bin/env python
# coding: utf-8

from datetime import datetime, timedelta
from bs4 import BeautifulSoup as soup
import csv
import requests
login_url = 'https://myaccount.nytimes.com/svc/ios/v2/login'
leaders_url = 'https://www.nytimes.com/puzzles/leaderboards'
username = ''
password = ''


players = ['Seibert', 'dirk orozco', 'Joshtreg', 'E-thousand']

with open('cookie.txt') as f:
    cookie = f.readlines()[0]
# Cookie manually added

# def login(username, password):
#     login_resp = requests.post(login_url, data = {'login': username,
#                                             'password': password},
#                                     headers = {'User-Agent': 'Mozilla/5.0',
#                                                'client_id': 'ios.crosswords'})
#     login_resp.raise_for_status()
#     for cookie in login_resp.json()['data']['cookies']:
#         if cookie['name'] == 'NYT-S':
#             return cookie['cipheredValue']
#     raise ValueError('NYT-S cookie not found')


def get_mini_times(cookie, output):
    response = requests.get(leaders_url, cookies={'NYT-S': cookie})
    page = soup(response.content, features='html.parser')
    solvers = page.find_all('div', class_='lbd-score')
    current_datetime = datetime.now()
    month = str(current_datetime.strftime("%m"))
    day = str(current_datetime.strftime("%d"))
    year = str(current_datetime.strftime("%Y"))
    daytimes = []
    # print('--------------------------')
    # print("Mini Times for " + month + '-' + day + '-' + year)
    for solver in solvers:
        name = solver.find('p', class_='lbd-score__name').text.strip()
        try:
            time = solver.find('p', class_='lbd-score__time').text.strip()
        except:
            time = "--"
        if name.endswith("(you)"):
            name_split = name.split()
            name = name_split[0]
        if name in players:
            if time == '--':
                time = ''
                seconds = ''
            else:
                t = datetime.strptime(time, "%M:%S")
                delta = timedelta(
                    hours=t.hour, minutes=t.minute, seconds=t.second)
                seconds = round(delta.total_seconds())
            daytimes.append(
                [month, day, year, f'{year}-{month}-{day}', name, time, seconds])
    with open(output, 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(daytimes)


get_mini_times(
    cookie, 'mini_data.csv')
