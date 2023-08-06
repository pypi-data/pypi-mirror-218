import json
import requests
import webbrowser

def title(id):
    try:
        data = json.loads(requests.get(f"https://api.scratch.mit.edu/project/{id}/").text)
        return (data["title"])
    except Exception as e:
        print("There is a error. Maybe the project is not shared or it does not exists.")
        return e

def description(id):
    try:
        data = json.loads(requests.get(f"https://api.scratch.mit.edu/project/{id}/").text)
        return (data["description"])
    except Exception as e:
        print("There is a error. Maybe the project is not shared or it does not exists.")
        return e
    
def views(id):
    try:
        data = jsondata = json.loads(requests.get(f"https://api.scratch.mit.edu/project/{id}/").text)
        return (data["stats"]['views'])
    except Exception as e:
        print("There is a error. Maybe the project is not shared or it does not exists.")
        return e
    
def loves(id):
    try:
        data = jsondata = json.loads(requests.get(f"https://api.scratch.mit.edu/project/{id}/").text)
        return (data["stats"]['loves'])
    except Exception as e:
        print("There is a error. Maybe the project is not shared or it does not exists.")
        return e
    
def favorites(id):
    try:
        data = jsondata = json.loads(requests.get(f"https://api.scratch.mit.edu/project/{id}/").text)
        return (data['stats']['favorites'])
    except Exception as e:
        print("There is a error. Maybe the project is not shared or it does not exists.")
        return e
    
def remixes(id):
    try:
        data = jsondata = json.loads(requests.get(f"https://api.scratch.mit.edu/project/{id}/").text)
        return (data["stats"]['remixes'])
    except Exception as e:
        print("There is a error. Maybe the project is not shared or it does not exists.")
        return e
    
def exists(id):
    try:
        data = jsondata = json.loads(requests.get(f"https://api.scratch.mit.edu/project/{id}/").text)
        if data['code'] == 'ResourceNotFound':
            return "Project is not shared or it does not exists."
        else:
            return 'There is a bad error. Please report to https://github.com/Tony14261/tscratchapiget/issues'
    except Exception:
            return 'Project exists'
    
def open(id):
    try:
        url = 'https://scratch.mit.edu/projects/' + id
        webbrowser.open_new(url=url)
        return "Opened successfully"
    except Exception:
        return "There is a bad error. Please report to https://github.com/Tony14261/tscratchapiget/issues"
