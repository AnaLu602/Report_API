import json
import os

def create_report(fileName='report.json'):
    if not os.path.exists(fileName):
        with open(fileName, 'x') as jsonFile:
            data = {"requests": []}
            json.dump(data, jsonFile)

def get_report_path(fileName='report.json'):
    if os.path.exists(fileName):
        return os.path.abspath(fileName)
    return -1

def update_report(fileName='report.json',json_request=None):
    with open(fileName, "r") as jsonFile:
            data = json.load(jsonFile)
            
    request_count = len(data["requests"])
    json_data = {"id": request_count}
        
    if json_request is not None:
        json_data.update(json_request)
    
    data["requests"].append(json_data)

    with open(fileName, "w") as jsonFile:
        json.dump(data, jsonFile)

def delete_report(fileName='report.json'):
    if os.path.exists(fileName):
        os.remove(fileName)
    pass