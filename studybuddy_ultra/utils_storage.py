import json

def load(file_path):
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except:
        return []

def save(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)