from fastapi import Form
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
def upload_file(
    student_name: str = Form(...),   # 👈 ADD HERE
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    
    # Check existing versions
    existing = db.query(models.File).filter(models.File.filename == file.filename).all()
    version = len(existing) + 1

    file_path = f"{UPLOAD_DIR}/{version}_{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 👇 JUST ADD student_name HERE
    new_file = models.File(
        filename=file.filename,
        version=version,
        filepath=file_path,
        student_name=student_name   # 👈 ADD THIS LINE
    )

    db.add(new_file)
    db.commit()
    db.refresh(new_file)

    return {
        "filename": file.filename,
        "version": version,
        "student_name": student_name
    }

@router.get("/files/")
def get_files(db: Session = Depends(get_db)):
    files = db.query(models.File).all()

    result = []
    for file in files:
        result.append({
            "filename": file.filename,
            "version": file.version,
            "uploaded_at": file.uploaded_at
        })

    return result

@router.get("/student/{name}")
def get_student_files(name: str, db: Session = Depends(get_db)):
    files = db.query(models.File).filter(models.File.student_name == name).all()
    return files