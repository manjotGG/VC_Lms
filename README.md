# 📁 LMS File Tracker

## 🚀 Project Overview
The LMS File Tracker is a backend system that enables version control for files uploaded in a university Learning Management System (LMS). It ensures that every file update is stored as a new version instead of overwriting the previous one.

---

## 🎯 Problem Statement
In traditional LMS systems, students and teachers exchange files without proper versioning, leading to confusion, data loss, and difficulty in tracking updates.

---

## ✅ Solution
This project implements a Git-inspired version control system where:
- Each uploaded file is stored as a new version
- Previous versions are preserved
- Users can track file history easily

---

## ⚙️ Features
- 📤 Upload files
- 🔁 Automatic versioning (v1, v2, v3...)
- 📜 Version history tracking
- 🕒 Timestamp for each upload
- 🗂 Organized file storage

---

## 🛠 Tech Stack
- Backend: FastAPI (Python)
- Database: SQLite / PostgreSQL
- ORM: SQLAlchemy
- Server: Uvicorn

---

## 📁 Project Structure
lms-file-tracker/
│
├── main.py
├── database.py
├── models.py
├── routes/
│ └── files.py
├── uploads/
└── requirements.txt
