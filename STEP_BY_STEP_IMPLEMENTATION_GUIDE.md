# Banking Web Application — Step-by-Step Implementation Guide

> **How to use this guide**
> Work through each section in order. Every step describes *what* to do and *why* — not the exact code to write.

---

## 1. Environment Setup

### 1.1 Prerequisites Check
- **Python 3.9 or higher**
- **pip**
- **A terminal / command prompt**
- **A modern web browser**

### 1.2 Project Folder Structure

See IMPLEMENTATION_PLAN.md for the full folder tree.

### 1.3 Virtual Environment

```bash
cd BACKEND
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### 1.4 Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 2. Running the Application

```bash
cd BACKEND
python app.py
```

Open http://127.0.0.1:5000 — login with `testuser` / `password123`.

---

## 3. Running Tests

```bash
cd BACKEND
python -m pytest tests/ -v
```

Expected: **29 passed**.

---

*End of Step-by-Step Implementation Guide*
