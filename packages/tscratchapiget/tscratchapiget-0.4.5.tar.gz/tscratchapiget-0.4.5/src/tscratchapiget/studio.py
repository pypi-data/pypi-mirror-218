import json
import requests

def title(id):
    data = json.loads(requests.get(f"https://api.scratch.mit.edu/studios/{id}/").text)
    try:
        return (data["title"])
    except Exception:
        print("There's a bad error wile getting studio title. Please check again the studio ID")
        return "Error: Can't find studio. Check the console."
    
def description(id):
    data = json.loads(requests.get(f"https://api.scratch.mit.edu/studios/{id}/").text)
    try:
        return data["description"]
    except Exception:
        print("There's a bad error while getting studio description. Please check again the studio ID")
        return "Error: Can't find studio. Check the console."
    
def comments_allowed(id):
    data = json.loads(requests.get(f"https://api.scratch.mit.edu/studios/{id}/").text)
    try:
        var = data["comments_allowed"]
        if var == 'true':
            return True
        else:
            return False
    except Exception:
        print("There's a bad error while getting if comments are allowed. Please check again the studio ID")
        return "Error: Can't find studio. Check the console."

def created(id):
    data = json.loads(requests.get(f"https://api.scratch.mit.edu/studios/{id}/").text)
    try:
        return data["history"]["created"]
    except Exception:
        print("There's a bad error while getting the create date. Please check again the studio ID")
        return "Error: Can't find studio. Check the console."
    
def comments(id):
    data = json.loads(requests.get(f"https://api.scratch.mit.edu/studios/{id}/").text)
    try:
        return data["stats"]["comments"]
    except Exception:
        print("There's a bad error while fetching comments. Please check again the studio ID")
        return "Error: Can't find studio. Check the console."
    
def followers():
    data = json.loads(requests.get(f"https://api.scratch.mit.edu/studios/{id}/").text)
    try:
        return data["stats"]["followers"]
    except Exception:
        print("There's a bad error while fetching studio number of followers. Please check again the studio ID")
        return "Error: Can't find studio. Check the console."
    
def projects():
    data = json.loads(requests.get(f"https://api.scratch.mit.edu/studios/{id}/").text)
    try:
        return data["stats"]["projects"]
    except Exception:
        print("There's a bad error while fetching number of projects. Please check again the studio ID")
        return "Error: Can't find studio. Check the console."

#def public(id):
    #data = json.loads(requests.get(f"https://api.scratch.mit.edu/studios/{id}/").text)
    #try:
        #return data["public"]
    #except Exception:
        #print("There's a bad error. Please check again the studio ID")
        #return "Error: Can't find studio"