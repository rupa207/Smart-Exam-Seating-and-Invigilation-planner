# Smart Exam Seating and Invigilation Planner

## Overview
Smart Exam Seating and Invigilation Planner is a Flask-based web application that automates exam seating arrangements and faculty allocation. It ensures fair distribution of students across halls by mixing branches and academic years, reducing malpractice and manual effort.

## Features
- Student Management (Add / Delete / CSV Upload)
- Hall Management (Rows, Columns, Capacity)
- Faculty Management (Manual + CSV Upload)
- Smart Seating Algorithm (Branch + Year Mixing)
- Automatic Faculty Allocation
- Bench-wise Seating Arrangement
- PDF Report Generation (Downloadable & Searchable)
- Admin Login System

## How It Works
1. Admin logs into the system  
2. Uploads students, halls, and faculty data  
3. System shuffles and groups students  
4. Allocates students across halls  
5. Assigns faculty automatically  
6. Displays seating arrangement  
7. Generates downloadable PDF report  

## Tech Stack
- Frontend: HTML, CSS  
- Backend: Flask (Python)  
- Database: SQLite  
- Libraries: Pandas, SQLAlchemy, ReportLab  

## Installation
```bash
pip install flask pandas sqlalchemy reportlab
python app.py
```

## CSV Format
### Students
roll_number,name,branch,year

### Faculty
name,department

### Halls
name,rows,columns

## Advantages
- Saves time and effort  
- Reduces human errors  
- Ensures fair seating  
- Easy data management  

## Future Enhancements
- AI-based seating  
- Multi-user support  
- Mobile app
  
## 📸 Screenshots
### Login
![Login](/Screenshots/login.png)

### Dashboard
![Dashboard](/Screenshots/dashboard.png)

### Students 
![Students](/Screenshots/Students.png)

### Halls
![Students](/Screenshots/halls.png)

### Faculty
![Faculty](/Screenshots/faculty.png)

### Seating
![Seating](/Screenshots/generate_seating.png)

### Report
![Report](/Screenshots/reports.png)

### PDF Report
![PDF](/Screenshots/reports_pdf.png)

## Developed By
Chenna Rupa Sree
