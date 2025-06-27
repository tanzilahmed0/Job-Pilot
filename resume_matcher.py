import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Mapping of resume filenames to the keywords that trigger them.
# The order matters: it will use the first one that matches.
RESUME_KEYWORDS = {
    "ml_engineer.pdf": ["machine learning", "ml engineer", "ml"],
    "data_scientist.pdf": ["data scientist", "data science"],
    "data_analyst.pdf": ["data analyst", "analyst"],
    "swe.pdf": ["software engineer", "swe", "software developer", "developer"],
}

DEFAULT_RESUME = "swe.pdf"

def match_resume(job: dict) -> str:
    """
    Selects the best resume for a job based on its title and description.

    Args:
        job: A dictionary containing the job's 'title' and 'description'.

    Returns:
        The full path to the best-matched resume PDF.
    """
    title = job.get('title', '').lower()
    description = job.get('description', '').lower()
    search_text = title + " " + description

    resume_base_path = os.getenv("RESUME_PATH", "resumes/")

    for resume_file, keywords in RESUME_KEYWORDS.items():
        for keyword in keywords:
            if keyword in search_text:
                return os.path.join(resume_base_path, resume_file)

    # If no specific keywords are found, return the path to the default resume
    return os.path.join(resume_base_path, DEFAULT_RESUME)

if __name__ == '__main__':
    # Ensure RESUME_PATH is set for the test, defaulting to "resumes/"
    if "RESUME_PATH" not in os.environ:
        os.environ["RESUME_PATH"] = "resumes/"

    test_jobs = [
        {"title": "Senior ML Engineer", "description": "Looking for a machine learning expert.", "expected": "resumes/ml_engineer.pdf"},
        {"title": "Software Engineer Intern", "description": "C++ and Python skills required.", "expected": "resumes/swe.pdf"},
        {"title": "Data Scientist", "description": "We need a data scientist for our team.", "expected": "resumes/data_scientist.pdf"},
        {"title": "Business Analyst", "description": "Requires data analysis and reporting.", "expected": "resumes/data_analyst.pdf"},
        {"title": "Product Manager", "description": "A non-technical role.", "expected": "resumes/swe.pdf"},
        {"title": "Data & ML Developer", "description": "Build machine learning pipelines.", "expected": "resumes/ml_engineer.pdf"},
        {"title": "iOS Developer", "description": "Mobile app development.", "expected": "resumes/swe.pdf"},
    ]

    print("--- Testing match_resume() ---")
    all_passed = True
    for job in test_jobs:
        result = match_resume(job)
        expected = job['expected']
        if result == expected:
            print(f"[PASS] Job '{job['title']}' -> '{result}'")
        else:
            print(f"[FAIL] Job '{job['title']}' -> '{result}' (Expected: '{expected}')")
            all_passed = False
            
    print("\n--- Resume Matcher Test Summary ---")
    if all_passed:
        print("All resume matcher tests passed!")
    else:
        print("Some resume matcher tests failed.")
