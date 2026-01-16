from flask import Flask, render_template, request, redirect, flash
from database.db import get_db_connection
from intelligence.predatory_detector import is_predatory
from intelligence.suitability_engine import calculate_suitability

app = Flask(__name__)
app.secret_key = "verifyed_secret_key"

# ------------------- HOME -------------------
@app.route("/")
def home():
    return render_template("home.html")


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
        name = request.form.get("name")
        email = request.form.get("email")
        degree = request.form.get("degree")
        branch = request.form.get("branch")
        year = request.form.get("year")
        skills = ", ".join(request.form.getlist("skills"))
        research_interests = ", ".join(request.form.getlist("research_interests"))

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = """
                INSERT INTO students (name, email, degree, branch, year, skills, research_interests)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (name, email, degree, branch, year, skills, research_interests))
            conn.commit()
            cursor.close()
            conn.close()
            flash(" Registration successful!", "success")
            return redirect("/register")
        except Exception as e:
            flash(f" Error: {e}", "danger")

    return render_template("register.html")


# ------------------- DASHBOARD -------------------
@app.route("/dashboard/<int:student_id>")
def dashboard(student_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM students WHERE student_id=%s", (student_id,))
        student = cursor.fetchone()
        if not student:
            return "Student not found"

        cursor.execute("SELECT * FROM opportunities")
        opportunities = cursor.fetchall()

        matched = []
        for opp in opportunities:
            # ===== DEBUG MODE: temporarily ignore predatory & suitability =====
            opp['match_score'] = 1
            matched.append(opp)

            # ===== REAL LOGIC =====
            # if not is_predatory(opp):
            #     opp['match_score'] = calculate_suitability(student, opp)
            #     if opp['match_score'] > 0:
            #         matched.append(opp)

        matched.sort(key=lambda x: x['match_score'], reverse=True)

        cursor.close()
        conn.close()

        # DEBUG PRINT
        print(f"DEBUG: {len(matched)} opportunities matched for student {student['name']}")
        for opp in matched[:10]:  # print first 10
            print(f"{opp['title']} | Score: {opp['match_score']}")

        return render_template("dashboard.html", student=student, opportunities=matched)

    except Exception as e:
        return f"Error: {e}"
# ------------------- GET ALL OPPORTUNITIES -------------------
def get_opportunities():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM opportunities ORDER BY deadline ASC")
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results
# ------------------- MAIN -------------------
if __name__ == "__main__":
    app.run(debug=True)