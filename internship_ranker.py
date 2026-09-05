
"""
internship_ranker.py

Ranks internship opportunities based on how well they match
the user's requested skill and location.

Scoring:
- Skill match        : 40 points
- Location match     : 30 points
- Title match        : 10 points
- Eligibility        : 10 points
- Stipend             : 5 points
- Duration            : 5 points

Maximum score: 100
"""

import re


def normalize(value):
    """Convert a value into clean lowercase text."""

    if value is None:
        return ""

    if isinstance(value, list):
        value = " ".join(str(item) for item in value)

    return str(value).strip().lower()


def words(text):
    """Extract useful words from text."""

    return set(
        re.findall(
            r"[a-zA-Z0-9+#.]+",
            normalize(text)
        )
    )


def skill_score(internship, keyword):
    """
    Score how strongly the requested skill matches
    the internship.
    """

    requested = normalize(keyword)

    if not requested:
        return 0

    title = normalize(
        internship.get("title", "")
    )

    skills = normalize(
        internship.get("skills", "")
    )

    description = normalize(
        internship.get("description", "")
    )

    requested_words = words(requested)

    if not requested_words:
        return 0

    score = 0

    # Exact skill field match
    if requested in skills:
        score += 40
        return score

    # Exact title match
    if requested in title:
        score += 35

    # Individual requested words
    matched_skill_words = sum(
        1
        for word in requested_words
        if word in skills
    )

    if matched_skill_words:
        score += min(
            30,
            matched_skill_words * 15
        )

    # Description match
    if requested in description:
        score += 10

    return min(score, 40)


def location_score(internship, requested_location):
    """
    Score location relevance.

    Priority:
    Exact location     = 30
    Same city mention  = 30
    Same state/region  = 20
    Remote             = 15
    India for India    = 15
    Otherwise          = 0
    """

    requested = normalize(
        requested_location
    )

    actual = normalize(
        internship.get("location", "")
    )

    if not requested or not actual:
        return 0

    # Exact requested location
    if requested == actual:
        return 30

    # Requested city appears in internship location
    if requested in actual:
        return 30

    # Common Karnataka matching
    karnataka_places = {
        "mangalore",
        "mangaluru",
        "bangalore",
        "bengaluru",
        "mysore",
        "mysuru",
        "hubli",
        "belgaum"
    }

    if (
        requested in karnataka_places
        and actual
    ):
        if any(
            place in actual
            for place in karnataka_places
        ):
            return 20

    # Remote internships are useful for India searches
    if "remote" in actual:
        if requested in {
            "india",
            "mangalore",
            "mangaluru",
            "bangalore",
            "bengaluru"
        }:
            return 15

    # India-level match
    if requested == "india" and "india" in actual:
        return 15

    return 0


def title_score(internship, keyword):
    """Score whether the requested skill appears in the title."""

    requested = normalize(keyword)
    title = normalize(
        internship.get("title", "")
    )

    if not requested or not title:
        return 0

    if requested in title:
        return 10

    requested_words = words(requested)

    matched = sum(
        1
        for word in requested_words
        if word in title
    )

    if matched:
        return min(
            7,
            matched * 4
        )

    return 0


def eligibility_score(internship):
    """Give points when meaningful eligibility information exists."""

    eligibility = normalize(
        internship.get("eligibility", "")
    )

    if not eligibility:
        return 0

    invalid_values = {
        "not available",
        "not specified",
        "unknown",
        "none",
        "n/a"
    }

    if eligibility in invalid_values:
        return 0

    return 10


def stipend_score(internship):
    """Give points when stipend information is available."""

    stipend = normalize(
        internship.get("stipend", "")
    )

    if not stipend:
        return 0

    invalid_values = {
        "not available",
        "not specified",
        "unknown",
        "none",
        "n/a"
    }

    if stipend in invalid_values:
        return 0

    # Paid internships get full points
    if (
        "₹" in stipend
        or "rs" in stipend
        or "inr" in stipend
        or "stipend" in stipend
        or "paid" in stipend
    ):
        return 5

    return 3


def duration_score(internship):
    """Give points when duration is available."""

    duration = normalize(
        internship.get("duration", "")
    )

    if not duration:
        return 0

    invalid_values = {
        "not available",
        "not specified",
        "unknown",
        "none",
        "n/a"
    }

    if duration in invalid_values:
        return 0

    return 5


def calculate_match_score(
    internship,
    keyword,
    location="India"
):
    """Calculate the final score from 0 to 100."""

    score = 0

    score += skill_score(
        internship,
        keyword
    )

    score += location_score(
        internship,
        location
    )

    score += title_score(
        internship,
        keyword
    )

    score += eligibility_score(
        internship
    )

    score += stipend_score(
        internship
    )

    score += duration_score(
        internship
    )

    return min(
        100,
        score
    )


def rank_internships(
    internships,
    keyword,
    location="India"
):
    """
    Rank internships from best match to weakest match.
    """

    if not isinstance(internships, list):
        return []

    ranked = []

    for internship in internships:

        if not isinstance(
            internship,
            dict
        ):
            continue

        item = internship.copy()

        item["match_score"] = calculate_match_score(
            internship,
            keyword,
            location
        )

        ranked.append(item)

    # Highest score first
    ranked.sort(
        key=lambda item: item.get(
            "match_score",
            0
        ),
        reverse=True
    )

    return ranked


# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    print("=" * 70)
    print("REALISTIC INTERNSHIP RANKER TEST")
    print("=" * 70)

    keyword = input(
        "Enter skill: "
    ).strip()

    location = input(
        "Enter location: "
    ).strip()

    if not keyword:
        keyword = "Python"

    if not location:
        location = "Mangalore"

    sample_internships = [

        {
            "title": "Python Developer Intern",
            "company": "Coastal Tech",
            "location": "Mangalore, Karnataka",
            "skills": "Python, Flask, SQL",
            "eligibility": "CSE/ISE students and freshers",
            "duration": "3 Months",
            "stipend": "₹15,000/month",
            "description": "Develop Python backend applications.",
            "apply_url": "https://example.com/1"
        },

        {
            "title": "Python Data Science Intern",
            "company": "Data Labs",
            "location": "Bangalore, Karnataka",
            "skills": "Python, Pandas, SQL",
            "eligibility": "Students with Python knowledge",
            "duration": "4 Months",
            "stipend": "₹12,000/month",
            "description": "Analyze datasets using Python.",
            "apply_url": "https://example.com/2"
        },

        {
            "title": "Machine Learning Intern",
            "company": "AI Labs",
            "location": "Hyderabad, India",
            "skills": "Python, Machine Learning, TensorFlow",
            "eligibility": "Students with ML knowledge",
            "duration": "6 Months",
            "stipend": "₹20,000/month",
            "description": "Build machine learning models using Python.",
            "apply_url": "https://example.com/3"
        },

        {
            "title": "Python Remote Internship",
            "company": "Remote Systems",
            "location": "Remote",
            "skills": "Python, APIs, Git",
            "eligibility": "Engineering students",
            "duration": "3 Months",
            "stipend": "Paid",
            "description": "Work remotely on Python projects.",
            "apply_url": "https://example.com/4"
        },

        {
            "title": "Frontend Development Intern",
            "company": "WebWorks",
            "location": "Pune, India",
            "skills": "HTML, CSS, JavaScript",
            "eligibility": "Web development students",
            "duration": "3 Months",
            "stipend": "₹10,000/month",
            "description": "Build modern web applications.",
            "apply_url": "https://example.com/5"
        }
    ]

    results = rank_internships(
        sample_internships,
        keyword,
        location
    )

    print()
    print(
        f"Best matches for '{keyword}' "
        f"in '{location}':"
    )
    print()

    for index, internship in enumerate(
        results,
        start=1
    ):

        print("-" * 70)

        print(
            f"{index}. {internship['title']}"
        )

        print(
            f"Company      : "
            f"{internship['company']}"
        )

        print(
            f"Location     : "
            f"{internship['location']}"
        )

        print(
            f"Skills       : "
            f"{internship['skills']}"
        )

        print(
            f"Match Score  : "
            f"{internship['match_score']}%"
        )

        print(
            f"Apply URL    : "
            f"{internship['apply_url']}"
        )

    print("-" * 70)
    print()
    print("RANKING TEST COMPLETED")
    print("=" * 70)

