from typing import Any
from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse, FileResponse
import src.utils
import os

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
    src.utils.create_report(filename)
    return JSONResponse(content="OK",status_code=200)


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
    src.utils.update_report(filename, json_request=json_request)
    return JSONResponse(content="OK",status_code=200)

@app.delete("/report")
def delete_report(
    *,
    filename: str = 'test.json',
    http_request: Request
) -> Any:
    src.utils.delete_report(filename)
    return JSONResponse(content="OK",status_code=200)