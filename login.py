import requests
import json
import pickle
import os
import re

TOKEN = 'YOUR_BOT_TOKEN_HERE'

panels = [
    {"url": "http://s1.example.com:1111/", "username": "user1", "password": "admin1"},
    {"url": "http://s1.example.com:2222/", "username": "user2", "password": "admin2"},
    {"url": "http://s1.example.com:3333/", "username": "user3", "password": "admin3"},
]

url_login = "login"
url_lists = "xui/inbound/list"
url_sanaei = "panel/inbound/list"

pickle_file = "cookies.pkl"
json_file = "data.json"

def write_pickle(pickle_data):
    with open(pickle_file, 'wb') as f:
        pickle.dump(pickle_data, f)

def file_exists(file_path):
    return os.path.exists(file_path)

def is_file_empty(file_path):
    return file_exists(file_path) and os.stat(file_path).st_size == 0

def get_data_from_panels():
    panels_data = {}
    cookies = {}

    if not file_exists(pickle_file):
        open(pickle_file, 'w').close()

    elif not is_file_empty(pickle_file):
        try:
            with open(pickle_file, 'rb') as f:
                cookies = pickle.load(f)
        except:
            open(pickle_file, 'w').close()

    for panel in panels:
        if panel['url'][-1] != '/':
            panel['url'] += '/'

        try:
            panel_name = re.findall(r"http.?://(.*):", panel['url'])[0]
        except IndexError:
            print(f"{panel['url']} : The URL structure is incorrect")
            continue

        payload = {
            "username": panel['username'],
            "password": panel['password']
        }

        session = requests.Session()

        if panel_name in cookies:
            session.cookies.update(cookies[panel_name])

        try:
            response = session.post(panel['url'] + url_login, data=payload)

            if response.status_code == 404:
                print(f"{panel_name} : Are you sure your panel doesn't have a path address?")
                continue
            elif not response.json().get('success', False):
                print(f"{panel_name} : Wrong Username or Password")
                continue

            cookies[panel_name] = response.cookies.get_dict()
            write_pickle(cookies)

            panel_data = session.post(panel['url'] + url_lists)
            if panel_data.status_code != 404:
                panels_data[panel_name] = panel_data.json()['obj']
            else:
                panels_data[panel_name] = session.post(panel['url'] + url_sanaei).json()['obj']

        except (requests.exceptions.InvalidURL, requests.exceptions.InvalidSchema, requests.exceptions.ConnectionError):
            print(f"{panel['url']} : incorrect URL or port number")
            continue

    return panels_data

def save_accounts_to_json():
    panels_data = get_data_from_panels()

    with open(json_file, 'w') as f:
        json.dump(panels_data, f, indent=4)

    print("Data saved successfully!")

def StartMYFILD():
    save_accounts_to_json()

if __name__ == '__main__':
    save_accounts_to_json()
