import uvicorn
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import os

# Create FastAPI app
app = FastAPI()

# Mount a static files directory to serve uploaded files
app.mount("/files", StaticFiles(directory="files"), name="files")


# Define a route to upload a file
@app.post("/uploadfile/")
async def upload_file(question: str, file: UploadFile = File(...)):
    file_location = f"files/{file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())
    return {"info": f"file '{file.filename}' saved at '{file_location}' with question '{question}'"}

if __name__ == "__main__":
    if not os.path.exists("../files"):
        os.makedirs("../files")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
