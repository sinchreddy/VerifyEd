from flask import Flask, render_template, request, redirect, flash
from database.db import get_db_connection
from intelligence.predatory_detector import is_predatory
from intelligence.suitability_engine import calculate_suitability
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session
from werkzeug.security import generate_password_hash
from flask import request, redirect, render_template, flash
from database.db import get_db_connection

app = Flask(__name__)
app.secret_key = "verifyed_secret_key"

# ------------------- HOME -------------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # 🔓 TEMP BYPASS LOGIN
        session["student_id"] = 1   # assume student_id = 1 exists
        session["email"] = email

        return redirect("/dashboard/1")

    return render_template("home.html")
"""
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        print("LOGIN EMAIL:", email)
        print("LOGIN PASSWORD:", password)

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM students WHERE email=%s", (email,))
        student = cursor.fetchone()

        cursor.close()
        conn.close()

        print("STUDENT FROM DB:", student)

        if student:
            print("HASH IN DB:", student["password"])
            print("CHECK:", check_password_hash(student["password"], password))

        if student and check_password_hash(student["password"], password):
            session["student_id"] = student["student_id"]
            return redirect(f"/dashboard/{student['student_id']}")
        else:
            flash("❌ Invalid email or password", "danger")
            return redirect("/")

    return render_template("home.html")
"""

# ------------------- TEST DATABASE -------------------
@app.route("/test-db")
def test_db():
    try:
        conn = get_db_connection()
        if conn.is_connected():
            return "Database connected successfully!"
        else:
            return " Database connection failed"
    except Exception as e:
        return f" Error: {e}"


# ------------------- STUDENT REGISTRATION -------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # 🔹 Fetch form data
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        degree = request.form.get("degree")
        branch = request.form.get("branch")
        year = request.form.get("year")
        skills = request.form.get("skills")
        research_interests = request.form.get("research_interests")

        # 🔹 DEBUG (VERY IMPORTANT)
        print("FORM DATA:", name, email, password, skills, research_interests)

        if not all([name, email, password]):
            flash("All required fields must be filled", "danger")
            return redirect("/register")

        hashed_password = generate_password_hash(password)

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO students
                (name, email, password, degree, branch, year, skills, research_interests)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
            """, (
                name,
                email,
                hashed_password,
                degree,
                branch,
                year,
                skills,
                research_interests
            ))

            conn.commit()
            flash("✅ Registration successful. Please login.", "success")
            return redirect("/")

        except Exception as e:
            conn.rollback()
            print("DB ERROR:", e)
            flash("❌ Email already exists or DB error", "danger")
            return redirect("/register")

        finally:
            cursor.close()
            conn.close()
    print(request.form)
    return render_template("register.html")

# ------------------- DASHBOARD -------------------
@app.route("/dashboard/<int:student_id>")
def dashboard(student_id):
    if "student_id" not in session:
        return redirect("/")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch student
    cursor.execute(
        "SELECT * FROM students WHERE student_id=%s",
        (student_id,)
    )
    student = cursor.fetchone()

    if not student:
        cursor.close()
        conn.close()
        return "Student not found"

    # Fetch ALL opportunities (no logic, no filters)
    cursor.execute("SELECT * FROM opportunities ORDER BY deadline ASC")
    opportunities = cursor.fetchall()

    cursor.close()
    conn.close()

    # 🔍 DEBUG PRINT
    print("TOTAL OPPORTUNITIES:", len(opportunities))
    for opp in opportunities:
        print(
            f"{opp.get('title')} | "
            f"{opp.get('type')} | "
            f"{opp.get('deadline')}"
        )

    return render_template(
        "dashboard.html",
        student=student,
        opportunities=opportunities
    )
# ------------------- GET ALL OPPORTUNITIES -------------------
def get_opportunities():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM opportunities ORDER BY deadline ASC")
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ------------------- MAIN -------------------
if __name__ == "__main__":
    app.run(debug=True)