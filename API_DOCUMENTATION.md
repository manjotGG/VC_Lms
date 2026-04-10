# 📚 LMS File Tracker - API Documentation

## 🎯 Teacher Workflow (As Specified in code.json)

```
1️⃣  Search Student (by name OR URN)
    ↓
2️⃣  View All Files of That Student
    ↓
3️⃣  Download Latest Version
```

---

## 🔌 API Endpoints

### 1. Upload File
**Endpoint:** `POST /upload/`

**Parameters (Form Data):**
- `student_name` (string, required) - Student name (will be converted to lowercase)
- `student_urn` (string, required) - Student URN (unique identifier)
- `file` (file, required) - File to upload
- `comment` (string, required) - Upload comments

**Response:**
```json
{
  "filename": "assignment.pdf",
  "version": 1,
  "student_name": "john doe",
  "student_urn": "URN123456",
  "comment": "First submission"
}
```

**File Naming Format:** `{student_urn}_{filename}_v{version}`
- Example: `URN123456_assignment.pdf_v1`

---

### 2. Search Student (TEACHER WORKFLOW STEP 1)
**Endpoint:** `GET /search/`

**Query Parameters:**
- `student_name` (string, optional) - Student name to search
- `student_urn` (string, optional) - Student URN to search
- **At least one parameter required**

**Response:**
```json
{
  "student_name": "john doe",
  "student_urn": "URN123456",
  "files": [
    {
      "filename": "assignment.pdf",
      "versions": [1, 2, 3]
    },
    {
      "filename": "report.docx",
      "versions": [1, 2]
    }
  ]
}
```

**Example Requests:**
```bash
# Search by name
curl "http://localhost:8000/search/?student_name=john%20doe"

# Search by URN
curl "http://localhost:8000/search/?student_urn=URN123456"
```

---

### 3. Get All Student Files (TEACHER WORKFLOW STEP 2)
**Endpoint:** `GET /student/files/`

**Query Parameters:**
- `student_name` (string, optional) - Student name
- `student_urn` (string, optional) - Student URN
- **At least one parameter required**

**Response:**
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
          "comment": "Updated version",
          "uploaded_at": "2026-04-10T14:00:00",
          "id": 2
        }
      ]
    }
  ]
}
```

**Example Request:**
```bash
curl "http://localhost:8000/student/files/?student_urn=URN123456"
```

---

### 4. Download Latest Version (TEACHER WORKFLOW STEP 3)
**Endpoint:** `GET /download/latest/`

**Query Parameters:**
- `student_urn` (string, required) - Student URN
- `filename` (string, required) - Filename to download

**Response:** Downloads the file (binary)

**Example Request:**
```bash
curl "http://localhost:8000/download/latest/?student_urn=URN123456&filename=assignment.pdf" -O
```

---

### 5. Download All Latest Files
**Endpoint:** `GET /download/all-latest/`

**Query Parameters:**
- `student_urn` (string, required) - Student URN

**Response:**
```json
{
  "student_urn": "URN123456",
  "total_files": 2,
  "files": [
    {
      "version": 3,
      "filepath": "uploads/URN123456_assignment.pdf_v3",
      "filename": "assignment.pdf",
      "comment": "Final version",
      "uploaded_at": "2026-04-10T16:00:00",
      "id": 3
    },
    {
      "version": 2,
      "filepath": "uploads/URN123456_report.docx_v2",
      "filename": "report.docx",
      "comment": "Complete",
      "uploaded_at": "2026-04-10T15:00:00",
      "id": 5
    }
  ]
}
```

---

### 6. Download by File ID
**Endpoint:** `GET /download/{file_id}`

**Path Parameters:**
- `file_id` (integer) - File record ID

**Response:** Downloads the file (binary)

---

### 7. Admin View (All Students & Files)
**Endpoint:** `GET /admin/`

**Query Parameters:** None

**Response:**
```json
{
  "total_students": 2,
  "students": [
    {
      "student_name": "john doe",
      "student_urn": "URN123456",
      "files": [
        {
          "filename": "assignment.pdf",
          "versions": [
            {
              "version": 1,
              "comment": "v1",
              "uploaded_at": "2026-04-10T10:00:00",
              "id": 1
            },
            {
              "version": 2,
              "comment": "v2",
              "uploaded_at": "2026-04-10T11:00:00",
              "id": 2
            }
          ]
        }
      ]
    }
  ]
}
```

---

### 8. Admin - List All Files
**Endpoint:** `GET /admin/files/`

**Response:**
```json
[
  {
    "id": 1,
    "filename": "assignment.pdf",
    "version": 1,
    "student_name": "john doe",
    "student_urn": "URN123456",
    "comment": "submission",
    "uploaded_at": "2026-04-10T10:00:00"
  }
]
```

---

### 9. Admin Summary
**Endpoint:** `GET /admin/summary`

**Response:**
```json
{
  "total_records": 5,
  "total_students": 2,
  "students": {
    "john doe": 3,
    "jane smith": 2
  }
}
```

---

## 🗂️ Database Schema

**Table: files**

| Field | Type | Description |
|-------|------|-------------|
| id | Integer (PK) | Auto-incremented ID (internal use) |
| filename | String | Original filename |
| version | Integer | Version number |
| filepath | String | File storage path |
| student_name | String | Student name (lowercase) |
| student_urn | String | Student URN (unique identifier) |
| comment | String | Upload comment |
| uploaded_at | DateTime | Upload timestamp |

---

## 📋 Version Control Logic

- **Per-Student Per-File:** Each student has independent version numbers for each file
- **Auto-Increment:** Uploading same filename for same student increments version
- **No Overwrite:** Previous versions are always preserved

**Example:**
```
Student: john doe (URN123456)
File: assignment.pdf
  - v1: Uploaded on 2026-04-10 10:00 (comment: "Initial")
  - v2: Uploaded on 2026-04-10 14:00 (comment: "Updated")
  - v3: Uploaded on 2026-04-10 16:00 (comment: "Final")

File: report.docx
  - v1: Uploaded on 2026-04-10 11:00 (comment: "Draft")
  - v2: Uploaded on 2026-04-10 15:00 (comment: "Complete")
```

---

## 🚀 Quick Start

### 1. Initialize Database
```bash
python init_db.py
```

### 2. Start Server
```bash
uvicorn main:app --reload
```

### 3. Access API Documentation
- Interactive Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## 💡 Key Features

✅ **Student Identification:**
- Use URN or name (both stored as lowercase)
- No file_id required for teacher operations

✅ **Teacher Workflow:**
- Search student
- View all files with version numbers
- Download latest version directly

✅ **Version Management:**
- Automatic versioning per student per file
- Latest version tracking
- All versions preserved

✅ **Admin Features:**
- Complete data view
- Student summary statistics
- File management

---

## ⚠️ Notes

- All student names are stored in **lowercase** for consistency
- Student URN is the primary unique identifier
- File IDs are for internal use only; teachers use URN + filename
- Latest version is automatically identified by highest version number
