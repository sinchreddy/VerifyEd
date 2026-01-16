def calculate_suitability(student, opportunity):
    """
    Returns a match score (0 or higher) for a student-opportunity pair
    based on skills, research interests, and eligibility.
    """

    # Handle None values
    student_skills = [s.strip().lower() for s in (student.get('skills') or "").split(',') if s.strip()]
    student_interests = [i.strip().lower() for i in (student.get('research_interests') or "").split(',') if i.strip()]
    
    # Get opportunity domains
    opp_domains = [d.strip().lower() for d in (opportunity.get('domains') or "").split(',') if d.strip()]
    
    # Match score = number of overlaps
    score = len(set(student_skills + student_interests) & set(opp_domains))
    
    # Extra rules
    if opportunity.get('type') == 'Hackathon' and int(student.get('year', 1)) < 2:
        score -= 1

    # Eligibility check (optional)
    eligibility = (opportunity.get('eligibility') or "").lower()
    degree = (student.get('degree') or "").lower()
    branch = (student.get('branch') or "").lower()
    if eligibility and degree not in eligibility and branch not in eligibility:
        score -= 1

    return max(score, 0)