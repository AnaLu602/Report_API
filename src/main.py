from typing import Any
from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse, FileResponse
import os
import json

app = FastAPI()

@app.get("/")
async def root():
    return {"Server says It's All Good"}

@app.post("/report")
def create_report(
    *,
    filename: str = 'test.json',
    http_request: Request
) -> Any:
    if not os.path.exists(filename):
        with open(filename, 'x') as jsonFile:
            data = {"requests": []}
            json.dump(data, jsonFile)
        return JSONResponse(content=f"Report named {filename} created",status_code=200)
    return JSONResponse(content=f"Report named {filename} already exists",status_code=409)


@app.get("/report")
def get_report(
    *,
    filename: str = 'test.json',
    http_request: Request
) -> Any:

    if not os.path.exists(filename):
        return JSONResponse(content="File not Found",status_code=404)
    
    report_path = os.path.abspath(filename)

    return FileResponse(report_path,filename=filename)

@app.put("/report")
async def update_report(
    *,
    filename: str = 'test.json',
    http_request: Request
) -> Any:
    json_request = await http_request.json()

    if not os.path.exists(filename):
        return JSONResponse(content="File not Found",status_code=404)

    with open(filename, "r") as jsonFile:
            data = json.load(jsonFile)
            
    request_count = len(data["requests"])
    json_data = {"id": request_count}
        
    if json_request is not None:
        json_data.update(json_request)
    
    data["requests"].append(json_data)

    with open(filename, "w") as jsonFile:
        json.dump(data, jsonFile)

    return JSONResponse(content="Report updated",status_code=200)

@app.delete("/report")
def delete_report(
    *,
    filename: str = 'test.json',
    http_request: Request
) -> Any:
    if os.path.exists(filename):
        os.remove(filename)
        return JSONResponse(content="Report deleted",status_code=200)
    return JSONResponse(content="File not Found",status_code=404)