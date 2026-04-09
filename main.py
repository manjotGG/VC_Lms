from fastapi import FastAPI
from routes import files

app = FastAPI()

app.include_router(files.router)

@app.get("/")
def home():
    return {"message": "LMS File Tracker Running 🚀"}