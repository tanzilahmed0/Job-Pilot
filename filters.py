import re
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# List of keywords that identify a role as an internship.
# Using regex word boundaries (\b) to avoid matching parts of words (e.g., "international").
INTERNSHIP_KEYWORDS = [
    r'\bintern\b',
    r'\binternship\b',
]

def is_internship_role(title: str) -> bool:
    """
    Checks if a job title indicates an internship role.

    Args:
        title: The job title string.

    Returns:
        True if the title contains internship-related keywords, False otherwise.
    """
    if not title:
        return False
    
    # Check if any of the keywords are present in the title (case-insensitive)
    for keyword in INTERNSHIP_KEYWORDS:
        if re.search(keyword, title, re.IGNORECASE):
            return True
    return False

def get_target_seasons() -> list[str]:
    """
    Gets the target seasons from the .env file and cleans them up.
    """
    seasons_str = os.getenv("TARGET_SEASONS", "")
    if not seasons_str:
        return []
    # Split by comma and strip whitespace from each season
    return [season.strip() for season in seasons_str.split(',')]

def is_valid_season(description: str) -> bool:
    """
    Checks if a job description mentions any of the target seasons.
    Args:
        description: The full job description text.
    Returns:
        True if a target season is found, False otherwise.
    """
    if not description:
        return False
    
    target_seasons = get_target_seasons()
    if not target_seasons:
        return False
        
    for season in target_seasons:
        # Use word boundaries to ensure we match whole words/phrases only
        if re.search(r'\b' + re.escape(season) + r'\b', description, re.IGNORECASE):
            return True
    return False

def is_valid_job(job: dict) -> bool:
    """
    Runs a job through all filters to check if it's a valid target.
    Args:
        job: A dictionary containing job 'title' and 'description'.
    Returns:
        True if the job passes all filters, False otherwise.
    """
    if not job or not isinstance(job, dict):
        return False
        
    title = job.get('title')
    description = job.get('description')

    if not is_internship_role(title):
        return False
    
    if not is_valid_season(description):
        return False
        
    return True

if __name__ == '__main__':
    # --- Test is_internship_role() ---
    test_titles = {
        "Software Engineer Intern": True,
        "Data Science Internship": True,
        "Product Manager (Intern)": True,
        "International Operations": False,
        "Senior Software Engineer": False,
        "Just a regular job": False,
        "Intern, Analytics": True,
        "": False,
        None: False,
    }

    print("--- Testing is_internship_role() ---")
    all_passed = True
    for title, expected in test_titles.items():
        result = is_internship_role(title)
        if result == expected:
            print(f"[PASS] '{title}' -> {result}")
        else:
            print(f"[FAIL] '{title}' -> {result} (Expected: {expected})")
            all_passed = False
            
    print("\n--- Role Test Summary ---")
    if all_passed:
        print("All role tests passed!")
    else:
        print("Some role tests failed.")

    # --- Test is_valid_season() ---
    # Assumes TARGET_SEASONS="Fall 2025, Summer 2026" from .env
    target_seasons_str = os.getenv("TARGET_SEASONS", "Not Set")
    print(f"\n--- Testing is_valid_season() with TARGET_SEASONS='{target_seasons_str}' ---")

    test_descriptions = {
        "This is an internship for Fall 2025. Apply now!": True,
        "We are looking for someone for our summer 2026 program.": True,
        "Join us in spring 2025. Or maybe fall 2025.": True,
        "Looking for a Spring 2024 intern.": False,
        "This role is for the Fall2025 session.": False, # No word boundary
        "No season mentioned here.": False,
        "This is for the summer 2025 internship cohort.": False,
        "": False,
        None: False,
    }

    season_tests_passed = True
    for desc, expected in test_descriptions.items():
        if desc is None:
            desc_preview = "None"
        else:
            desc_preview = f"'{desc[:30]}...'"
        
        result = is_valid_season(desc)
        if result == expected:
            print(f"[PASS] Description {desc_preview} -> {result}")
        else:
            print(f"[FAIL] Description {desc_preview} -> {result} (Expected: {expected})")
            season_tests_passed = False
            
    print("\n--- Season Test Summary ---")
    if season_tests_passed:
        print("All season tests passed!")
    else:
        print("Some season tests failed.")

    # --- Test is_valid_job() ---
    print("\n--- Testing is_valid_job() ---")
    test_jobs = [
        # Should Pass: Correct role and season
        {"title": "Software Engineer Intern", "description": "Apply for our Fall 2025 program.", "expected": True},
        # Should Fail: Correct role, wrong season
        {"title": "Data Science Internship", "description": "This is for Spring 2024.", "expected": False},
        # Should Fail: Wrong role, correct season
        {"title": "Senior Product Manager", "description": "This is for Summer 2026.", "expected": False},
        # Should Fail: Wrong role, wrong season
        {"title": "Senior Engineer", "description": "A full-time job.", "expected": False},
        # Should Pass: One of multiple seasons is correct
        {"title": "Intern, Marketing", "description": "We need someone for Spring 2025 or Fall 2025.", "expected": True},
        # Should Fail: Missing description
        {"title": "Intern, Sales", "description": None, "expected": False},
        # Should Fail: Missing title
        {"title": None, "description": "Looking for Fall 2025.", "expected": False},
        # Should Fail: Empty object
        {"title": None, "description": None, "expected": False},
    ]

    job_tests_passed = True
    for job in test_jobs:
        result = is_valid_job(job)
        expected = job['expected']
        if result == expected:
            print(f"[PASS] Job '{job['title']}' -> {result}")
        else:
            print(f"[FAIL] Job '{job['title']}' -> {result} (Expected: {expected})")
            job_tests_passed = False
            
    print("\n--- Job Filter Test Summary ---")
    if job_tests_passed:
        print("All job filter tests passed!")
    else:
        print("Some job filter tests failed.")
