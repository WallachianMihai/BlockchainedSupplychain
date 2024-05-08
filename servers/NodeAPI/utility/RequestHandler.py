import requests

def GET(URL: str):
    return requests.get(URL).json()

def POST(URL: str, data):
    return requests.post(url=URL, json=data).json()