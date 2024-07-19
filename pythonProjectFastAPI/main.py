import uvicorn
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import os
from docquery import document, pipeline
import pandas as pd

# Create FastAPI app
app = FastAPI()

# Mount a static files directory to serve uploaded files
app.mount("/files", StaticFiles(directory="files"), name="files")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize docquery pipeline
p = pipeline('document-question-answering')

# Route to serve the HTML page
@app.get("/", response_class=HTMLResponse)
async def get_homepage():
    return FileResponse("static/index.html")

# Define a route to upload a file and process a question
@app.post("/uploadfile/")
async def upload_file(question: str = Form(...), top_k: int = Form(...), file: UploadFile = File(...)):
    file_location = f"files/{file.filename}"

    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())

    doc = document.load_document(file_location)
    answers = p(question=question, **doc.context, top_k=top_k)

    response = {
        "file": file.filename,
        "question": question,
        "answers": [
            {"answer": answer["answer"], "score": answer["score"], "page": answer["page"] + 1}
            for answer in answers
        ]
    }

    return JSONResponse(response)

# Ensure the 'files' directory exists
if __name__ == "__main__":
    if not os.path.exists("files"):
        os.makedirs("files")
    if not os.path.exists("static"):
        os.makedirs("static")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
