#Main code that has uploads as POST(1) and GET(3)

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

    '''
    with open(file_location, "wb") as f:
        f.write(await file.read())
    return {"filename": file.filename}




# Define a route to access a file by name
@app.get("/file/{filename}")
def get_file(filename: str):
    file_path = os.path.join("files", filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(file_path)

# Define a route to list all uploaded files
@app.get("/files/")
def list_files():
    files = os.listdir("files")
    return {"files": files}


# Serve the HTML form for file upload
@app.get("/", response_class=HTMLResponse)
def upload_form():
    files = os.listdir("files")
    files_list = "".join(f"<li><a href='/files/{file}'>{file}</a></li>" for file in files)
    return f"""
    <html>
        <body>
            <h2>Upload File</h2>
            <form action="/uploadfile/" enctype="multipart/form-data" method="post">
                <input name="file" type="file">
                <input type="submit">
            </form>
            <h3>Uploaded Files</h3>
            <ul>
                {files_list}
            </ul>
        </body>
    </html>
    """
'''

if __name__ == "__main__":
    if not os.path.exists("files"):
        os.makedirs("files")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
