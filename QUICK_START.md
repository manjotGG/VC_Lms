# 🚀 Quick Start Guide

## Prerequisites
- Python 3.7+ installed
- FastAPI, SQLAlchemy, Uvicorn installed (see requirements below)

## Setup Instructions

### 1. Install Dependencies
```bash
cd /Users/manjotsingh/Downloads/New_/VC_Lms
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt  # If requirements.txt exists
# Or install manually:
# pip install fastapi uvicorn sqlalchemy
```

### 2. Initialize Database
```bash
python init_db.py
# Output: Database created ✅
```

### 3. Start the Server
```bash
uvicorn main:app --reload
# Server running at: http://127.0.0.1:8000
```

### 4. Test the API
Visit: http://127.0.0.1:8000/docs (interactive API documentation)

---

## Example API Usage

### Upload a File
```bash
curl -X POST "http://127.0.0.1:8000/upload/" \
  -F "student_name=john doe" \
  -F "student_urn=URN123456" \
  -F "file=@myfile.txt" \
  -F "comment=Assignment v1"
```

### Query Student Files
```bash
curl "http://127.0.0.1:8000/student/?student_urn=URN123456&student_name=john doe"
```

### Get Latest Version
```bash
curl "http://127.0.0.1:8000/latest/?student_urn=URN123456&filename=myfile.txt"
```

### Download Latest File
```bash
curl "http://127.0.0.1:8000/download/latest/?student_urn=URN123456&filename=myfile.txt" -O
```

### View All Files (Admin)
```bash
curl "http://127.0.0.1:8000/admin/files/"
```

---

## File Storage
- Uploaded files are stored in: `./uploads/` directory
- File naming format: `{student_urn}_{filename}_v{version}`
- Example: `URN123456_essay.txt_v1`

---

## Database Schema
**Table: files**
- id (Integer, Primary Key)
- filename (String)
- version (Integer)
- filepath (String)
- student_name (String, lowercase)
- student_urn (String, unique identifier)
- comment (String)
- uploaded_at (DateTime)

---

## All Issues Fixed ✅
See [FIXES_SUMMARY.md](FIXES_SUMMARY.md) for detailed changes.
