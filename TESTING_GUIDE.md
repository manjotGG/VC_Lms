# 🧪 LMS File Tracker - Testing Guide

## 📝 Teacher Workflow Test Guide

Follow these steps to test the complete teacher workflow!

---

## Step 1: Start the Server

```bash
cd /Users/manjotsingh/Downloads/New_/VC_Lms
source venv/bin/activate
python init_db.py  # Initialize database if first time
uvicorn main:app --reload
```

**Server will run at:** http://localhost:8000
**API Docs:** http://localhost:8000/docs

---

## Step 2: Upload Sample Files

### Upload File 1 (John Doe - Assignment v1)
```bash
curl -X POST "http://localhost:8000/upload/" \
  -F "student_name=John Doe" \
  -F "student_urn=URN123456" \
  -F "file=@assignment.pdf" \
  -F "comment=Initial submission"
```

### Upload File 2 (John Doe - Assignment v2)
```bash
curl -X POST "http://localhost:8000/upload/" \
  -F "student_name=John Doe" \
  -F "student_urn=URN123456" \
  -F "file=@assignment.pdf" \
  -F "comment=Updated with corrections"
```

### Upload File 3 (John Doe - Report)
```bash
curl -X POST "http://localhost:8000/upload/" \
  -F "student_name=John Doe" \
  -F "student_urn=URN123456" \
  -F "file=@report.docx" \
  -F "comment=Project report"
```

### Upload File 4 (Jane Smith - Assignment v1)
```bash
curl -X POST "http://localhost:8000/upload/" \
  -F "student_name=Jane Smith" \
  -F "student_urn=URN789012" \
  -F "file=@assignment.pdf" \
  -F "comment=First version"
```

---

## Step 3: Teacher Workflow - Step 1: SEARCH STUDENT

### Search by StudentURN
```bash
curl "http://localhost:8000/search/?student_urn=URN123456"
```

**Expected Response:**
```json
{
  "student_name": "john doe",
  "student_urn": "URN123456",
  "files": [
    {
      "filename": "assignment.pdf",
      "versions": [1, 2]
    },
    {
      "filename": "report.docx",
      "versions": [1]
    }
  ]
}
```

### Search by Student Name
```bash
curl "http://localhost:8000/search/?student_name=john%20doe"
```

---

## Step 4: Teacher Workflow - Step 2: VIEW ALL FILES

```bash
curl "http://localhost:8000/student/files/?student_urn=URN123456"
```

**Expected Response:**
```json
{
  "student_name": "john doe",
  "student_urn": "URN123456",
  "files": [
    {
      "filename": "assignment.pdf",
      "versions": [
        {
          "version": 1,
          "comment": "Initial submission",
          "uploaded_at": "2026-04-10T10:00:00",
          "id": 1
        },
        {
          "version": 2,
          "comment": "Updated with corrections",
          "uploaded_at": "2026-04-10T11:00:00",
          "id": 2
        }
      ]
    },
    {
      "filename": "report.docx",
      "versions": [
        {
          "version": 1,
          "comment": "Project report",
          "uploaded_at": "2026-04-10T12:00:00",
          "id": 3
        }
      ]
    }
  ]
}
```

---

## Step 5: Teacher Workflow - Step 3: DOWNLOAD LATEST

### Download Latest Assignment
```bash
curl "http://localhost:8000/download/latest/?student_urn=URN123456&filename=assignment.pdf" -O
```

**Result:** Downloaded file will be named `assignment.pdf` (latest version v2)

### Download Latest Report
```bash
curl "http://localhost:8000/download/latest/?student_urn=URN123456&filename=report.docx" -O
```

---

## Step 6: Download All Latest Files

```bash
curl "http://localhost:8000/download/all-latest/?student_urn=URN123456"
```

**Response:**
```json
{
  "student_urn": "URN123456",
  "total_files": 2,
  "files": [
    {
      "version": 2,
      "filepath": "uploads/URN123456_assignment.pdf_v2",
      "filename": "assignment.pdf",
      "comment": "Updated with corrections",
      "uploaded_at": "2026-04-10T11:00:00",
      "id": 2
    },
    {
      "version": 1,
      "filepath": "uploads/URN123456_report.docx_v1",
      "filename": "report.docx",
      "comment": "Project report",
      "uploaded_at": "2026-04-10T12:00:00",
      "id": 3
    }
  ]
}
```

---

## Step 7: Admin View

```bash
curl "http://localhost:8000/admin/"
```

### List All Files (Admin)
```bash
curl "http://localhost:8000/admin/files/"
```

### Get Summary
```bash
curl "http://localhost:8000/admin/summary"
```

**Expected Response:**
```json
{
  "total_records": 4,
  "total_students": 2,
  "students": {
    "john doe": 3,
    "jane smith": 1
  }
}
```

---

## 🔍 Testing with FastAPI Docs

### Interactive Testing
1. Navigate to: http://localhost:8000/docs
2. Each endpoint has a "Try it out" button
3. Fill in parameters and click "Execute"
4. See response immediately

### Available in Docs:
- ✅ POST /upload/
- ✅ GET /search/
- ✅ GET /student/files/
- ✅ GET /download/latest/
- ✅ GET /download/all-latest/
- ✅ GET /download/{file_id}
- ✅ GET /admin/
- ✅ GET /admin/files/
- ✅ GET /admin/summary

---

## 📊 File Storage Structure

After uploads, check the `uploads/` directory:

```
uploads/
├── URN123456_assignment.pdf_v1
├── URN123456_assignment.pdf_v2
├── URN123456_report.docx_v1
└── URN789012_assignment.pdf_v1
```

---

## ✅ Complete Workflow Checklist

- [ ] Server running on http://localhost:8000
- [ ] Database initialized
- [ ] Sample files uploaded
- [ ] Search by URN works ✓
- [ ] View all files works ✓
- [ ] Download latest works ✓
- [ ] Admin view accessible ✓
- [ ] Files stored in uploads/ ✓
- [ ] Version numbers correct ✓
- [ ] Student names lowercase ✓

---

## 🐛 Troubleshooting

### Port 8000 Already in Use
```bash
# Kill process using port 8000
lsof -ti:8000 | xargs kill -9

# Or use different port
uvicorn main:app --port 8001 --reload
```

### Database Error
```bash
# Reset database
rm test.db
python init_db.py
```

### File Not Found
- Check uploads/ directory exists
- Verify file was successfully uploaded
- Check filename and student_urn match

---

## 🎓 Expected Behavior

| Scenario | Action | Expected Result |
|----------|--------|-----------------|
| First upload | Upload same file by same student | version = 1 |
| Second upload | Upload same file by same student | version = 2 |
| Different file | Upload different file by same student | new filename, version = 1 |
| Download latest | Request latest of file with v1, v2, v3 | Returns v3 |
| Search by name | Search "John Doe" | Returns "john doe" (lowercase) |
| Search by URN | Search "URN123456" | Returns all files for that URN |
