def is_predatory(opportunity):
    """
    Returns True if the conference/hackathon is likely predatory.
    """

    trusted_publishers = ['IEEE', 'Springer', 'ACM', 'MLH', 'Devpost', 'HackerEarth']
    
    # 1. Publisher check
    if opportunity['organizer'] not in trusted_publishers:
        return True

    # 2. Indexed check
    if opportunity.get('indexed', 0) == 0:
        return True

    # 3. Unrealistic deadlines or fees
    if opportunity.get('deadline') and "2020" in opportunity['deadline']:  # example
        return True

    return False