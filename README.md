# Smart-Exam-Seating-and-Invigilation-planner
Smart Exam Seating and Invigilation Planner is a Flask-based web application that automates exam hall seating and faculty allocation. It ensures fair distribution of students by mixing branches and years, supports CSV uploads, and generates structured, searchable PDF reports, reducing manual effort and errors.
#🎯 Features
🔹 Student Management (Add / Delete / CSV Upload)
🔹 Hall Management (Rows, Columns, Capacity)
🔹 Faculty Management (Manual + CSV Upload)
🔹 Smart Seating Algorithm (Branch + Year Mixing)
🔹 Automatic Faculty Allocation
🔹 Bench-wise Seating Arrangement
🔹 PDF Report Generation (Downloadable & Searchable)
🔹 Admin Login System
#🧠 How It Works
Admin logs into the system
Uploads students, halls, and faculty data
System shuffles and groups students
Allocates students across halls
Assigns faculty automatically
Displays seating arrangement
Generates downloadable PDF report
#🛠️ Tech Stack
Frontend: HTML, CSS
Backend: Flask (Python)
Database: SQLite
Libraries:
Pandas (CSV handling)
SQLAlchemy (ORM)
ReportLab (PDF generation)
#⚙️ Installation & Setup
1️⃣ Clone the repository
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
2️⃣ Install dependencies
pip install flask pandas sqlalchemy reportlab
3️⃣ Run the application
python app.py
4️⃣ Open in browser
http://127.0.0.1:5000
#📂 CSV Format
Students CSV
roll_number,name,branch,year
21CS001,Ravi,CSE,3
21EC002,Anu,ECE,3
Faculty CSV
name,department
Ramesh,CSE
Suresh,EEE
Halls CSV
name,rows,columns
E101,6,3
E102,6,3
#📊 Output
Hall-wise seating display
Bench-wise student allocation
Faculty assigned per hall
Downloadable PDF report
#✅ Advantages
Saves time and effort
Reduces human errors
Ensures fair seating
Easy data management
Scalable for large institutions
#⚠️ Limitations
Requires correct CSV format
Basic UI (can be enhanced)
Single admin system
#🚀 Future Enhancements
Advanced UI/UX improvements
AI-based seating optimization
Multi-user/admin support
Search & filter features
Email notifications
Mobile application
#📸 Screenshots

(Add your project screenshots here for better presentation)

#📖 References
Flask Documentation
SQLAlchemy Documentation
Pandas Documentation
ReportLab Documentation
👨‍💻 Developed By

Chenna Rupa Sree

#🙏 Acknowledgement

Thanks to all mentors and resources that helped in building this project.

⭐ Don’t forget to star the repo if you like it!
