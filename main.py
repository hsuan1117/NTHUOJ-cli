import json
import time
import typer

import requests
import sys
import os
from bs4 import BeautifulSoup
import argparse
from rich import print

NTHUOJ_DIR = os.path.join(os.path.expanduser('~'), '.nthuoj')
NTHUOJ_CONFIG = os.path.join(NTHUOJ_DIR, 'config.json')

if not os.path.exists(NTHUOJ_DIR):
    os.makedirs(NTHUOJ_DIR)

if not os.path.exists(NTHUOJ_CONFIG):
    username = input('Please enter your username: ')
    password = input('Please enter your password: ')

    with open(NTHUOJ_CONFIG, 'w') as f:
        f.write(json.dumps({
            'username': username,
            'password': password
        }))

#####################
#  Main Functions   #
#####################
session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) ',
    'Referer': 'https://acm.cs.nthu.edu.tw/users/login/?next=/',
})
session.get('https://acm.cs.nthu.edu.tw/users/login/?next=/')


# check token exists
def check_token():
    config = json.load(open(NTHUOJ_CONFIG, 'r'))

    if 'token' in config:
        session.cookies['sessionid'] = config['token']
        r = session.get('https://acm.cs.nthu.edu.tw/status?username={}'.format(config['username']))
        if "No submissions found for the given query!" not in r.text:
            return
        else:
            del session.cookies['sessionid']

    print('[INFO] Re-login...')

    # token expired or not exists
    username = config['username']
    password = config['password']

    r = session.post('https://acm.cs.nthu.edu.tw/users/login/?next=/', data={
        'csrfmiddlewaretoken': session.cookies['csrftoken'],
        'username': username,
        'password': password
    })
    if r.status_code != 200:
        print('[ERROR] Login failed')
        return
    json.dump({
        'username': username,
        'password': password,
        'token': session.cookies['sessionid']
    }, open(NTHUOJ_CONFIG, 'w'))


check_token()


def submit(pid : str, code : str, lang : str = typer.Argument('CPP', help="The language you want to use")):
    if lang not in ['CPP', 'C', 'CPP11', 'CPP14', 'CPP17', 'Python']:
        print('[ERROR] Invalid language')
        return
    config = json.load(open(NTHUOJ_CONFIG, 'r'))
    r = session.post('https://acm.cs.nthu.edu.tw/users/submit/', data={
        'csrfmiddlewaretoken': session.cookies['csrftoken'],
        'pid': pid,
        'code': open(code, 'r').read(),
        'language': lang
    })
    if r.status_code != 200:
        print('[ERROR] Submit failed')
        return
    else:
        print('[INFO] [blue]Submit success[/blue]')
        print(
            f"[INFO] [blue]You can go to https://acm.cs.nthu.edu.tw/status/?username={config['username']} to check your submission status[/blue]")

        for i in range(10):
            r = session.get('https://acm.cs.nthu.edu.tw/status/?username={}'.format(config['username']))
            if r.status_code != 200:
                print('[ERROR] Get status failed')
                return
            else:
                soup = BeautifulSoup(r.text, 'html.parser')
                status = soup.find('table').find_all('tr')[1].find_all('td')[4].text.strip().replace('\n', '').replace(
                    '                   ', '')

                sys.stdout.write("\r{1}{0}".format("." * i if status == 'Being Judged' else '', status))
                sys.stdout.flush()

                if status != 'Being Judged':
                    break
            time.sleep(1)

if __name__ == "__main__":
    typer.run(submit)

