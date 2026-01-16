# VerifyEd – Student Opportunity Intelligence Bot

## Project Goal
**VerifyEd** is a student-centric intelligence platform that helps college students discover hackathons and research conferences (IEEE, ACM, Springer, MLH, Devpost, HackerEarth) relevant to their profile. It filters opportunities, detects predatory conferences, calculates suitability, and provides important details like deadlines and registration links.

## Features Implemented

### 1. Student Registration
- Students can register with details:
  - Name, Email
  - Degree, Branch, Year
  - Skills
  - Research Interests

### 2. Database Storage
- MySQL database stores:
  - Student details (`students` table)
  - Opportunities (`opportunities` table)
- Each opportunity includes:
  - Title, Type, Organizer, Platform, Domains
  - Deadline, Registration / Info Link
  - Indexed flag

### 3. Opportunity Fetching Pipeline (`fetch_opportunities.py`)
- Pulls conferences and hackathons from multiple sources:
  - IEEE (RSS feed)
  - ACM (RSS feed)
  - Springer (Web scraping)
  - MLH Hackathons
  - Devpost / HackerEarth (optional, JS-heavy pages may require Selenium)
- Stores all opportunities in the database
- Sample hackathons seeded for testing:
  - Smart India Hackathon
  - NASA Space Apps Challenge

### 4. Flask Web App (`app.py`)
- Routes implemented:
  - `/` → Home page
  - `/register` → Student registration
  - `/dashboard/<student_id>` → Student dashboard showing matched opportunities
- Opportunities are filtered using:
  - `is_predatory(opp)` → removes predatory conferences
  - `calculate_suitability(student, opp)` → calculates match score
- Dashboard displays:
  - Title, Type, Organizer, Domains, Deadline, Registration Link, Match Score

### 5. Debug Mode
- While setting up, the dashboard shows all opportunities with `match_score = 1` to test functionality
- Predatory detection and suitability scoring can be enabled later for production

## Current Improvements / Work in Progress
1. **Deadlines & Links**
   - Some RSS sources currently missing deadlines
   - Devpost/HackerEarth may require Selenium to fetch JavaScript-rendered content
   - Links to registration / conference page added wherever available

2. **Domains / Tags**
   - Many opportunities currently show “General” domain
   - Next step: extract actual domain info from RSS tags or conference page metadata

3. **Dashboard UX Enhancements**
   - Add filters: Hackathons only / Conferences only / Domain-based filtering
   - Add pagination for large datasets
   - Style with Bootstrap or Tailwind for better readability

4. **Predatory Filtering & Match Score**
   - Currently, debug mode bypasses scoring and filtering
   - Once fully integrated, only relevant and non-predatory opportunities will appear

## Folder Structure
<pre>
Verifyed/
├── app.py                 # Main Flask app
├── fetch_opportunities.py # Script to fetch hackathons and conferences
├── database/
│   └── db.py              # MySQL DB connection helper
├── intelligence/
│   ├── predatory_detector.py      # Detects predatory conferences
│   └── suitability_engine.py      # Calculates match score
├── templates/
│   ├── home.html
│   ├── register.html
│   ├── dashboard.html
│   └── dashboard_select.html      # Optional student selection page
└── README.md
</pre>

## How to Run
1. Clone the repository
   ```bash
   git clone <your-repo-url>
   cd Verifyed
2.	Setup Python environment
    python -m venv venv
    source venv/bin/activate      # Linux/Mac
    venv\Scripts\activate         # Windows
    pip install -r requirements.txt
3.	Configure MySQL database
	•	Create database verifyed_db
	•	Update credentials in database/db.py
4.	Run the opportunity fetcher
    python fetch_opportunities.py
5.	Start the Flask app
    python app.py
6.	Open browser
    http://127.0.0.1:5000