import requests

BASE_URL = "http://127.0.0.1:8000/"

ENDPOINT = "api/family/"


def get_list():

    r = requests.get(BASE_URL + ENDPOINT)

    status_code = r.status_code
    if status_code != 200:
        print('probably not good sign')

    data = r.json()
    links = []
    for i in data:
        for j in i['data']:
            links.append(j)

    return links

print(get_list())