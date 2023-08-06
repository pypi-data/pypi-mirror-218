import json
import requests

def title(id):
    data = json.loads(requests.get(f"https://api.scratch.mit.edu/studios/{id}/").text)
    try:
        return (data["title"])
    except Exception:
        print("There's a bad error. Please check again the studio ID")
        return "Error: Can't find studio"
    
def description(id):
    data = json.loads(requests.get(f"https://api.scratch.mit.edu/studios/{id}/").text)
    try:
        return data["description"]
    except Exception:
        print("There's a bad error. Please check again the studio ID")
        return "Error: Can't find studio"