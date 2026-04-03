from flask import Flask, render_template, request, redirect, session
from models import db, Student, Hall, Faculty
import pandas as pd
import csv
import random
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from flask import send_file
import io
app = Flask(__name__)
app.secret_key = "secret123"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

# ================= LOGIN =================
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

@app.route('/', methods=['GET','POST'])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin'] = True
            return redirect('/dashboard')

    return render_template("login.html")


# ================= DASHBOARD =================
@app.route('/dashboard')
def dashboard():
    if 'admin' not in session:
        return redirect('/')

    return render_template(
        "dashboard.html",
        students=Student.query.count(),
        halls=Hall.query.count(),
        faculty=Faculty.query.count()
    )


# ================= STUDENTS =================
@app.route('/students', methods=['GET', 'POST'])
def students():
    if request.method == 'POST':
        new_student = Student(
            name=request.form['name'],
            roll_number=request.form['roll_number'],
            branch=request.form['branch'],
            year=request.form['year']
        )
        db.session.add(new_student)
        db.session.commit()

    return render_template('students.html', students=Student.query.all())


@app.route('/delete_student/<int:id>')
def delete_student(id):
    student = Student.query.get(id)
    if student:
        db.session.delete(student)
        db.session.commit()
    return redirect('/students')


@app.route('/upload_csv', methods=['POST'])
def upload_csv():
    file = request.files['file']

    if file:
        df = pd.read_csv(file)
        df.columns = df.columns.str.strip()

        for _, row in df.iterrows():
            existing = Student.query.filter_by(roll_number=row['roll_number']).first()

            if not existing:
                db.session.add(Student(
                    roll_number=row['roll_number'],
                    name=row['name'],
                    branch=row['branch'],
                    year=row['year']
                ))

        db.session.commit()

    return redirect('/students')


# ================= HALLS =================
@app.route('/halls')
def halls():
    return render_template("halls.html", halls=Hall.query.all())


@app.route("/add_hall", methods=["POST"])
def add_hall():
    db.session.add(Hall(
        name=request.form["name"],
        rows=int(request.form["rows"]),
        columns=int(request.form["columns"])
    ))
    db.session.commit()
    return redirect('/halls')


@app.route('/upload_halls_csv', methods=['POST'])
def upload_halls_csv():
    file = request.files['file']

    if file.filename == "":
        return redirect('/halls')

    df = pd.read_csv(file)
    df.columns = df.columns.str.strip()

    for _, row in df.iterrows():
        existing = Hall.query.filter_by(name=row['name']).first()

        if not existing:
            db.session.add(Hall(
                name=row['name'],
                rows=int(row['rows']),
                columns=int(row['columns'])
            ))

    db.session.commit()
    return redirect('/halls')


# ================= FACULTY =================
@app.route("/faculty", methods=["GET", "POST"])
def faculty():
    if request.method == "POST":
        db.session.add(Faculty(
            name=request.form["name"],
            department=request.form["department"]
        ))
        db.session.commit()

    return render_template("faculty.html", faculty=Faculty.query.all())
@app.route("/upload_faculty_csv", methods=["POST"])
def upload_faculty_csv():
    file = request.files["file"]

    if not file:
        return "No file uploaded"

    import pandas as pd
    df = pd.read_csv(file)

    # clean columns
    df.columns = df.columns.str.strip().str.lower()

    print("Columns:", df.columns)

    for _, row in df.iterrows():

        # 🔥 handle multiple possible names
        name = (
            row.get("name") or
            row.get("faculty name") or
            row.get("faculty_name")
        )

        dept = (
            row.get("department") or
            row.get("dept") or
            row.get("department name")
        )

        if not name or not dept:
            print("Skipped:", row)
            continue

        db.session.add(Faculty(
            name=str(name).strip(),
            department=str(dept).strip()
        ))

    db.session.commit()
    return redirect("/faculty")
# ================= SEATING =================
@app.route('/seating')
def seating():
    return render_template("seating.html")


@app.route("/generate_seating")
def generate_seating():

    students = Student.query.all()
    halls = Hall.query.all()
    faculty_list = Faculty.query.all()

    if not students:
        return "No students found"
    if not halls:
        return "No halls found"
    if not faculty_list:
        return "No faculty found"

    # prepare students
    student_list = []
    for s in students:
        student_list.append({
            "roll": s.roll_number,
            "branch": s.branch,
            "year": s.year
        })

    random.shuffle(student_list)

    # mix by branch + year
    group = {}
    for s in student_list:
        key = (s["branch"], s["year"])
        group.setdefault(key, []).append(s)

    mixed_students = []
    while any(group.values()):
        for key in group:
            if group[key]:
                mixed_students.append(group[key].pop())

    seating = []
    index = 0
    faculty_index = 0

    for hall in halls:
        total_seats = hall.rows * hall.columns * 2
        hall_students = mixed_students[index:index + total_seats]
        index += total_seats

        benches = []
        for i in range(0, len(hall_students), 2):
            benches.append(hall_students[i:i+2])

        assigned_faculty = faculty_list[faculty_index % len(faculty_list)]
        faculty_index += 1

        seating.append({
            "hall": hall.name,
            "faculty": assigned_faculty.name,
            "benches": benches
        })

    return render_template("seating.html", seating=seating)


# ================= REPORTS =================
@app.route('/reports')
def reports():
    return render_template("reports.html")
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from flask import send_file
import io

@app.route("/download_report")
def download_report():

    students = Student.query.all()
    halls = Hall.query.all()
    faculty_list = Faculty.query.all()

    if not students or not halls or not faculty_list:
        return "Missing data"

    # ===== SAME SEATING LOGIC =====
    student_list = []
    for s in students:
        student_list.append({
            "roll": s.roll_number,
            "branch": s.branch,
            "year": s.year
        })

    import random
    random.shuffle(student_list)

    group = {}
    for s in student_list:
        key = (s["branch"], s["year"])
        group.setdefault(key, []).append(s)

    mixed_students = []
    while any(group.values()):
        for key in group:
            if group[key]:
                mixed_students.append(group[key].pop())

    seating = []
    index = 0
    faculty_index = 0

    for hall in halls:
        total_seats = hall.rows * hall.columns * 2
        hall_students = mixed_students[index:index + total_seats]
        index += total_seats

        benches = []
        for i in range(0, len(hall_students), 2):
            benches.append(hall_students[i:i+2])

        assigned_faculty = faculty_list[faculty_index % len(faculty_list)]
        faculty_index += 1

        seating.append({
            "hall": hall.name,
            "faculty": assigned_faculty.name,
            "benches": benches
        })

    # ===== BEAUTIFUL PDF =====
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()

    elements = []

    # 🔥 TITLE
    elements.append(Paragraph("<b><font size=18 color='darkblue'>Exam Seating Arrangement Report</font></b>", styles['Title']))
    elements.append(Spacer(1, 20))

    # 🔥 EACH HALL
    for hall in seating:

        elements.append(Paragraph(f"<b><font size=14 color='green'>Hall: {hall['hall']}</font></b>", styles['Heading2']))
        elements.append(Paragraph(f"<b>Faculty:</b> {hall['faculty']}", styles['Normal']))
        elements.append(Spacer(1, 10))

        # 🔥 TABLE DATA
        table_data = [["Bench", "Student 1", "Student 2"]]

        for i, bench in enumerate(hall['benches']):
            s1 = bench[0]["roll"] if len(bench) > 0 else ""
            s2 = bench[1]["roll"] if len(bench) > 1 else ""
            table_data.append([f"B{i+1}", s1, s2])

        table = Table(table_data)

        # 🔥 STYLE
        table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.grey),
            ('TEXTCOLOR',(0,0),(-1,0),colors.white),

            ('ALIGN',(0,0),(-1,-1),'CENTER'),

            ('GRID', (0,0), (-1,-1), 1, colors.black),

            ('BACKGROUND',(0,1),(-1,-1),colors.whitesmoke)
        ]))

        elements.append(table)
        elements.append(Spacer(1, 25))

    doc.build(elements)

    buffer.seek(0)
    return send_file(buffer, as_attachment=True,
                     download_name="seating_report.pdf",
                     mimetype='application/pdf')
# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True)