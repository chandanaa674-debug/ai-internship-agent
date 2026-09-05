
"""
prompts.py

This file contains the instructions used by the
AI Internship Agent.
"""


# ==========================================================
# SYSTEM PROMPT
# ==========================================================

SYSTEM_PROMPT = """
You are an AI Internship Recommendation Agent.

Your job is to help students find the most relevant
internship opportunities based on their requirements.

You may consider:

- Skill or technology
- Location
- Eligibility
- Experience level
- Stipend
- Duration
- Internship type
- Remote or onsite preference
- Match score

IMPORTANT RULES:

1. Never invent internship information.
2. Never invent a company name.
3. Never invent a stipend.
4. Never invent an application URL.
5. Never invent eligibility requirements.
6. Use only the information provided by the internship system.
7. Prefer internships with stronger skill matches.
8. Prefer the user's requested location when available.
9. Use the match score to help rank recommendations.
10. Clearly say when information is unavailable.

When presenting recommendations, give:

- Internship title
- Company
- Location
- Skills
- Eligibility
- Duration
- Stipend
- Internship type
- Match score
- Application URL
- A short explanation of why it matches

Keep the response clear, useful, and student-friendly.
"""


# ==========================================================
# USER PROMPT BUILDER
# ==========================================================

def build_user_prompt(
    keyword,
    location="India",
    internships=None
):
    """
    Create the prompt containing the student's requirements
    and the available internship results.
    """

    keyword = str(
        keyword or ""
    ).strip()

    location = str(
        location or "India"
    ).strip()

    internships = internships or []

    internship_text = []

    for number, internship in enumerate(
        internships,
        start=1
    ):

        internship_text.append(
            f"""
INTERNSHIP {number}

Title:
{internship.get("title", "Not Available")}

Company:
{internship.get("company", "Not Available")}

Location:
{internship.get("location", "Not Available")}

Skills:
{internship.get("skills", "Not Available")}

Eligibility:
{internship.get("eligibility", "Not Available")}

Duration:
{internship.get("duration", "Not Available")}

Stipend:
{internship.get("stipend", "Not Available")}

Type:
{internship.get("type", "Not Available")}

Match Score:
{internship.get("match_score", 0)}%

Description:
{internship.get("description", "Not Available")}

Apply URL:
{internship.get("apply_url", "")}
"""
        )

    if internship_text:
        available_internships = "\n".join(
            internship_text
        )
    else:
        available_internships = (
            "No internship results are available."
        )

    return f"""
STUDENT REQUIREMENTS

Skill:
{keyword}

Location:
{location}


AVAILABLE INTERNSHIPS

{available_internships}


TASK

Based only on the information above:

1. Identify the strongest internship matches.
2. Prefer higher match scores.
3. Prefer the requested location.
4. Prefer internships that match the requested skill.
5. Mention important eligibility information.
6. Mention stipend and duration when available.
7. Include internship type when available.
8. Give a short reason why each recommended internship is suitable.
9. Include the real application URL when available.
10. Do not invent missing information.

Return the recommendations in order from best match to weakest match.
"""


# ==========================================================
# SIMPLE RESPONSE FORMAT
# ==========================================================

RESPONSE_FORMAT = """
For each recommended internship, use this structure:

1. Internship Title
   Company:
   Location:
   Skills:
   Eligibility:
   Duration:
   Stipend:
   Type:
   Match Score:
   Why it matches:
   Apply URL:
"""


# ==========================================================
# DIRECT TEST
# ==========================================================

if __name__ == "__main__":

    print("=" * 70)
    print("INTERNSHIP AGENT - PROMPTS TEST")
    print("=" * 70)

    keyword = input(
        "Enter internship skill: "
    ).strip()

    location = input(
        "Enter location: "
    ).strip()

    if not keyword:
        keyword = "Python"

    if not location:
        location = "Bangalore"

    # Sample data only for testing this file.
    sample_internships = [

        {
            "title": "Python Developer Intern",
            "company": "Tech Solutions",
            "location": "Bangalore",
            "skills": "Python, Flask, SQL",
            "eligibility": "CSE students and freshers",
            "duration": "3 Months",
            "stipend": "₹15,000/month",
            "type": "On-site",
            "match_score": 95,
            "description": "Python backend development internship.",
            "apply_url": "https://example.com/apply"
        },

        {
            "title": "Data Science Intern",
            "company": "Data Labs",
            "location": "Bangalore",
            "skills": "Python, Pandas, SQL",
            "eligibility": "Students with Python knowledge",
            "duration": "4 Months",
            "stipend": "₹12,000/month",
            "type": "Hybrid",
            "match_score": 88,
            "description": "Analyze datasets using Python.",
            "apply_url": "https://example.com/data"
        }
    ]

    print()
    print("=" * 70)
    print("SYSTEM PROMPT")
    print("=" * 70)
    print(SYSTEM_PROMPT)

    print()
    print("=" * 70)
    print("GENERATED USER PROMPT")
    print("=" * 70)

    user_prompt = build_user_prompt(
        keyword,
        location,
        sample_internships
    )

    print(user_prompt)

    print()
    print("=" * 70)
    print("RESPONSE FORMAT")
    print("=" * 70)
    print(RESPONSE_FORMAT)

    print()
    print("=" * 70)
    print("PROMPTS TEST COMPLETED SUCCESSFULLY")
    print("=" * 70)
