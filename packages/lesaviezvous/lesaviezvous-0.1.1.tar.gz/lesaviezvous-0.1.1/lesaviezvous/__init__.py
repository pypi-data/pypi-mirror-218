import requests

def get_info():
    url = 'https://lesaviezvous.onrender.com/infos'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None