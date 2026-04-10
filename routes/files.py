from fastapi.responses import FileResponse
from fastapi import Form, Query
from fastapi import APIRouter, UploadFile, File, Depends
import shutil
import os
from sqlalchemy.orm import Session
from database import SessionLocal
import models
from collections import defaultdict

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
    student_name: str = Form(...),   
    student_urn: str = Form(...),
    file: UploadFile = File(...),
    comment: str = Form(...),
    db: Session = Depends(get_db)
):
    """Upload a file with automatic versioning"""
    student_name = student_name.strip().lower() 
    
    existing = db.query(models.File).filter(
        models.File.filename == file.filename,
        models.File.student_urn == student_urn
    ).all()
    version = len(existing) + 1

    file_path = f"{UPLOAD_DIR}/{student_urn}_{file.filename}_v{version}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    new_file = models.File(
        filename=file.filename,
        version=version,
        filepath=file_path,
        student_name=student_name,
        student_urn=student_urn,
        comment=comment
    )

    db.add(new_file)
    db.commit()
    db.refresh(new_file)

    return {
        "filename": file.filename,
        "version": version,
        "student_name": student_name,
        "student_urn": student_urn,
        "comment": comment
    }


@router.get("/search/")
def search_student(
    student_name: str = Query(None),
    student_urn: str = Query(None),
    db: Session = Depends(get_db)
):
    """Search student by name OR URN"""
    if not student_name and not student_urn:
        return {"error": "Provide student_name or student_urn"}
    
    query = db.query(models.File)
    
    if student_name:
        student_name = student_name.strip().lower()
        query = query.filter(models.File.student_name == student_name)
    
    if student_urn:
        query = query.filter(models.File.student_urn == student_urn)
    
    files = query.all()
    
    if not files:
        return {"error": "No files found"}
    
    student = files[0]
    files_dict = defaultdict(list)
    for f in files:
        files_dict[f.filename].append(f.version)
    
    for filename in files_dict:
        files_dict[filename].sort()
    
    return {
        "student_name": student.student_name,
        "student_urn": student.student_urn,
        "files": [{"filename": fn, "versions": v} for fn, v in files_dict.items()]
    }


@router.get("/student/files/")
def get_student_all_files(
    student_name: str = Query(None),
    student_urn: str = Query(None),
    db: Session = Depends(get_db)
):
    """Get all files for a student (by name OR URN)"""
    if not student_name and not student_urn:
        return {"error": "Provide student_name or student_urn"}
    
    query = db.query(models.File)
    
    if student_name:
        student_name = student_name.strip().lower()
        query = query.filter(models.File.student_name == student_name)
    
    if student_urn:
        query = query.filter(models.File.student_urn == student_urn)
    
    files = query.all()
    
    if not files:
        return {"error": "No files found"}
    
    student = files[0]
    files_dict = defaultdict(list)
    for f in files:
        files_dict[f.filename].append({
            "version": f.version,
            "comment": f.comment,
            "uploaded_at": f.uploaded_at,
            "id": f.id
        })
    
    for filename in files_dict:
        files_dict[filename].sort(key=lambda x: x["version"])
    
    return {
        "student_name": student.student_name,
        "student_urn": student.student_urn,
        "files": [{"filename": fn, "versions": v} for fn, v in files_dict.items()]
    }


@router.get("/download/latest/")
def download_latest_file(
    student_urn: str, 
    filename: str, 
    db: Session = Depends(get_db)
):
    """Download the latest version of a specific file"""
    file = db.query(models.File).filter(
        models.File.student_urn == student_urn,
        models.File.filename == filename
    ).order_by(models.File.version.desc()).first()

    if not file:
        return {"error": "File not found"}

    return FileResponse(path=file.filepath, filename=file.filename)


@router.get("/download/all-latest/")
def download_all_latest(student_urn: str, db: Session = Depends(get_db)):
    """Download all latest versions"""
    files = db.query(models.File).filter(
        models.File.student_urn == student_urn
    ).all()
    
    if not files:
        return {"error": "No files found"}
    
    latest_files = {}
    for f in files:
        if f.filename not in latest_files or f.version > latest_files[f.filename]["version"]:
            latest_files[f.filename] = {
                "version": f.version,
                "filepath": f.filepath,
                "filename": f.filename,
                "comment": f.comment,
                "uploaded_at": f.uploaded_at,
                "id": f.id
            }
    
    return {
        "student_urn": student_urn,
        "total_files": len(latest_files),
        "files": list(latest_files.values())
    }


@router.get("/download/{file_id}")
def download_file(file_id: int, db: Session = Depends(get_db)):
    """Download a specific file by ID"""
    file = db.query(models.File).filter(models.File.id == file_id).first()
    if not file:
        return {"error": "File not found"}
    return FileResponse(path=file.filepath, filename=file.filename)


@router.get("/admin/")
def admin_view(db: Session = Depends(get_db)):
    """Admin view of all students and files"""
    files = db.query(models.File).all()
    
    if not files:
        return {"error": "No files in database"}
    
    students_dict = defaultdict(lambda: {"student_urn": None, "files": {}})
    
    for f in files:
        student_key = f.student_name
        students_dict[student_key]["student_urn"] = f.student_urn
        
        if f.filename not in students_dict[student_key]["files"]:
            students_dict[student_key]["files"][f.filename] = []
        
        students_dict[student_key]["files"][f.filename].append({
            "version": f.version,
            "comment": f.comment,
            "uploaded_at": f.uploaded_at,
            "id": f.id
        })
    
    result = []
    for student_name, student_data in students_dict.items():
        files_list = []
        for filename, versions in student_data["files"].items():
            versions.sort(key=lambda x: x["version"])
            files_list.append({"filename": filename, "versions": versions})
        
        result.append({
            "student_name": student_name,
            "student_urn": student_data["student_urn"],
            "files": files_list
        })
    
    return {"total_students": len(result), "students": result}


@router.get("/admin/files/")
def admin_files(db: Session = Depends(get_db)):
    """List all files in database"""
    files = db.query(models.File).all()
    return [
        {
            "id": f.id,
            "filename": f.filename,
            "version": f.version,
            "student_name": f.student_name,
            "student_urn": f.student_urn,
            "comment": f.comment,
            "uploaded_at": f.uploaded_at
        }
        for f in files
    ]


@router.get("/admin/summary")
def summary(db: Session = Depends(get_db)):
    """Summary statistics"""
    files = db.query(models.File).all()
    data = {}
    for f in files:
        key = f.student_name
        data[key] = data.get(key, 0) + 1
    
    return {
        "total_records": len(files),
        "total_students": len(data),
        "students": data
    }
