from fastapi import APIRouter, UploadFile, File, Depends
import shutil
import os
from sqlalchemy.orm import Session
from database import SessionLocal
import models

router = APIRouter()

UPLOAD_DIR = "uploads"

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/upload/")
def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    
    # Check existing versions
    existing = db.query(models.File).filter(models.File.filename == file.filename).all()
    version = len(existing) + 1

    file_path = f"{UPLOAD_DIR}/{version}_{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    new_file = models.File(
        filename=file.filename,
        version=version,
        filepath=file_path
    )

    db.add(new_file)
    db.commit()
    db.refresh(new_file)

    return {"filename": file.filename, "version": version}