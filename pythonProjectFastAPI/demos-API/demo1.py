from fastapi import FastAPI, File, UploadFile, Request
import uvicorn
import shutil
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
app = FastAPI()
templates = Jinja2Templates(directory="templates")
@app.get("/upload/", response_class=HTMLResponse)
async def upload(request: Request):
   return templates.TemplateResponse("uploadfile.html", {"request": request})

if __name__ == "__main__":
   uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
