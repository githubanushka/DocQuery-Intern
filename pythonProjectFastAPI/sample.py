#Front end 1

import uvicorn
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse, JSONResponse
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


# Route to serve the HTML page
@app.get("/", response_class=HTMLResponse)
async def get_homepage():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Document Question Answering</title>
    </head>
    <body>
        <h1>Upload a Document and Ask a Question</h1>
        <form id="upload-form" action="/uploadfile/" method="post" enctype="multipart/form-data">
            <label for="file">Choose a file:</label>
            <input type="file" id="file" name="file" required><br><br>
            <label for="question">Enter your question:</label>
            <input type="text" id="question" name="question" required><br><br>
            <label for="top_k">Number of answers (top_k):</label>
            <input type="number" id="top_k" name="top_k" value="1" min="1" required><br><br>
            <button type="submit">Submit</button>
        </form>
        <h2>Response</h2>
        <pre id="response"></pre>

        <script>
            document.getElementById('upload-form').onsubmit = async function(event) {
                event.preventDefault();

                const formData = new FormData();
                formData.append('file', document.getElementById('file').files[0]);
                formData.append('question', document.getElementById('question').value);
                formData.append('top_k', document.getElementById('top_k').value);

                const responseElement = document.getElementById('response');
                responseElement.textContent = 'Processing...';

                try {
                    const response = await fetch('/uploadfile/', {
                        method: 'POST',
                        body: formData
                    });

                    if (!response.ok) {
                        throw new Error(`HTTP error! Status: ${response.status}`);
                    }

                    const data = await response.json();
                    responseElement.textContent = JSON.stringify(data, null, 2);
                } catch (error) {
                    responseElement.textContent = `Error: ${error.message}`;
                }
            };
        </script>
    </body>
    </html>
    """


# Define a route to upload a file and process a question
@app.post("/uploadfile/")
async def upload_file(question: str = Form(...), top_k: int = Form(...), file: UploadFile = File(...)):
    print(f"Question: {question}")
    #print(f"Top K: {top_k}")
    file_location = f"files/{file.filename}"

    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())

    #print(f"File saved at: {file_location}")

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

    return JSONResponse(response)


# Ensure the 'files' directory exists
if __name__ == "__main__":
    if not os.path.exists("files"):
        os.makedirs("files")
    uvicorn.run("sample:app", host="127.0.0.1", port=8000, reload=True)
