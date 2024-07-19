# Perfect DocQuery functioning on swagger UI

import uvicorn
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import os
from docquery import document, pipeline
import pandas as pd

# Create FastAPI app
app = FastAPI()

# Mount a static files directory to serve uploaded files
app.mount("/files", StaticFiles(directory="files"), name="files")

# Initialize docquery pipeline
p = pipeline('document-question-answering')

# Define a route to upload a file and process a question
@app.post("/uploadfile/")
async def upload_file(question: str, top_k: int, file: UploadFile = File(...)):
    print(f"Question: {question}")
    print(f"Top K: {top_k}")
    file_location = f"files/{file.filename}"

    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())

    print(f"File saved at: {file_location}")

    # Process the document using docquery
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

    # Print the answers
    for answer in response["answers"]:
        print(f"Answer: {answer['answer']}, Score: {answer['score']}, Page: {answer['page']}")

    return response

# Ensure the 'files' directory exists
if __name__ == "__main__":
    if not os.path.exists("files"):
        os.makedirs("files")
    uvicorn.run("save:app", host="127.0.0.1", port=8000, reload=True)
