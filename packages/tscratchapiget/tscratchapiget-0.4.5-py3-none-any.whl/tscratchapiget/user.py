import requests
import json
import webbrowser

global message_count
global id
global scratchteam
global join
global pfp_link
global pfp_link_open
global aboutme
global wiwo
global country
global followers
global following
global exist

def message_count(username):
    data = json.loads(requests.get(f"https://api.scratch.mit.edu/users/{username}/messages/count/").text)
    try:
        if data['code'] == 'NotFound':
            print('User does not exist')
            return 'Error'
    except Exception:
        return (data["count"])

def id(username):
    data = json.loads(requests.get(f"https://api.scratch.mit.edu/users/{username}/").text)
    try:
        if data['code'] == 'NotFound':
            print('User does not exist')
            return 'Error'
    except Exception:
        return (data["id"])

def scratchteam(username):
    data = json.loads(requests.get(f"https://api.scratch.mit.edu/users/{username}/").text)
    try:
        if data['code'] == 'NotFound':
            print('User does not exist')
            return 'Error'
    except Exception:
        return (data["scratchteam"])

def join(username):
    data = json.loads(requests.get(f"https://api.scratch.mit.edu/users/{username}/").text)
    try:
        if data['code'] == 'NotFound':
            print('User does not exist')
            return 'Error'
    except Exception:
        return (data['history'])

def pfp_link(username):
    data = json.loads(requests.get(f"https://api.scratch.mit.edu/users/{username}/").text)
    try:
        if data['code'] == 'NotFound':
            print('User does not exist')
            return 'Error'
    except Exception:
        return (data['profile']['images']['90x90'])

def pfp_link_open(username):
    data = json.loads(requests.get(f"https://api.scratch.mit.edu/users/{username}/").text)
    try:
        if data['code'] == 'NotFound':
            print('User does not exist')
            return 'Error'
    except Exception:
        webbrowser.open_new(data['profile']['images']['90x90'])

def aboutme(username):
    data = json.loads(requests.get(f"https://api.scratch.mit.edu/users/{username}/").text)
    try:
        if data['code'] == 'NotFound':
            print('User does not exist')
            return 'Error'
    except Exception:
        return (data['status'])

def wiwo(username): #What im working on
    data = json.loads(requests.get(f"https://api.scratch.mit.edu/users/{username}/").text)
    try:
        if data['code'] == 'NotFound':
            print('User does not exist')
            return 'Error'
    except Exception:
        return (data['bio'])

def country(username):
    data = json.loads(requests.get(f"https://api.scratch.mit.edu/users/{username}/").text)
    try:
        if data['code'] == 'NotFound':
            print('User does not exist')
            return 'Error'
    except Exception:
        return (data['country'])

def followers(username):
    data = json.loads(requests.get(f"https://scratchdb.lefty.one/v3/user/info/{username}/").text)
    try:
        if data['code'] == 'NotFound':
            print('User does not exist')
            return 'Error'
    except Exception:
        return (data['statistics']['followers'])

def following(username):
    data = json.loads(requests.get(f"https://scratchdb.lefty.one/v3/user/info/{username}/").text)
    try:
        if data['code'] == 'NotFound':
            print('User does not exist')
            return 'Error'
    except Exception:
        return (data['statistics']['following'])

def exist(username):
    data = json.loads(requests.get(f"https://api.scratch.mit.edu/users/{username}/").text)
    try:
        if data['code'] == 'NotFound':
            print('User does not exist')
            return 'Error'
    except Exception:
            return 'User exists'