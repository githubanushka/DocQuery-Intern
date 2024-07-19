'''
import requests
age=12
gender="M"

response=requests.get(f"http://127.0.0.1:8000/predict?age=12&gender=M")
output=response.json()

print(output)
'''

# Import required Library
import uvicorn
from fastapi import FastAPI

# creating fastAPI app
app = FastAPI()


# Define a route to serve a user
@app.get("/predict")
def predict_model(age:int,gender:str):
	if age<18 or gender=='F':
		return {'survived':1}
	else:
		return {'survived': 0}


if __name__ == "__main__":
   uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)


#uvicorn main:app --reload
#uvicorn main:app --reload
3