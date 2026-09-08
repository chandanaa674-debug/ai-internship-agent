
import requests
import re
from html import unescape


# =========================================================
# ARBEITNOW API
# =========================================================

API_URL = "https://www.arbeitnow.com/api/job-board-api"


# =========================================================
# KEYWORD ALIASES
# =========================================================

KEYWORD_ALIASES = {

    "python": [
        "python",
        "python developer",
        "python intern",
        "python internship"
    ],

    "java": [
        "java",
        "java developer",
        "java intern",
        "java internship"
    ],

    "machine learning": [
        "machine learning",
        "machine learning intern",
        "ml",
        "ml engineer"
    ],

    "ai": [
        "artificial intelligence",
        "ai",
        "ai intern",
        "ai engineer"
    ],

    "data science": [
        "data science",
        "data scientist",
        "data science intern"
    ],

    "data analyst": [
        "data analyst",
        "data analytics",
        "analytics intern"
    ],

    "web development": [
        "web developer",
        "web development",
        "frontend",
        "backend",
        "full stack",
        "fullstack"
    ],

    "javascript": [
        "javascript",
        "js",
        "react",
        "node",
        "frontend"
    ],

    "dsa": [
        "data structures",
        "algorithms",
        "dsa",
        "competitive programming"
    ]
}


# =========================================================
# LOCATION ALIASES
# =========================================================

LOCATION_ALIASES = {

    "india": [
        "india",
        "indian",
        "remote"
    ],

    "bangalore": [
        "bangalore",
        "bengaluru",
        "remote"
    ],

    "bengaluru": [
        "bangalore",
        "bengaluru",
        "remote"
    ],

    "mangalore": [
        "mangalore",
        "mangaluru",
        "remote"
    ],

    "mangaluru": [
        "mangalore",
        "mangaluru",
        "remote"
    ],

    "mumbai": [
        "mumbai",
        "bombay",
        "remote"
    ],

    "delhi": [
        "delhi",
        "new delhi",
        "remote"
    ],

    "hyderabad": [
        "hyderabad",
        "remote"
    ],

    "chennai": [
        "chennai",
        "madras",
        "remote"
    ],

    "pune": [
        "pune",
        "remote"
    ],

    "remote": [
        "remote",
        "work from home",
        "wfh"
    ]
}


# =========================================================
# CLEAN HTML
# =========================================================

def clean_text(value):

    if value is None:
        return ""

    if isinstance(value, list):

        return ", ".join(
            clean_text(item)
            for item in value
        )

    if isinstance(value, dict):

        return " ".join(
            clean_text(v)
            for v in value.values()
        )

    text = str(value)

    text = unescape(text)

    text = re.sub(
        r"<[^>]+>",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# =========================================================
# GET FIRST AVAILABLE FIELD
# =========================================================

def get_first_value(data, keys):

    for key in keys:

        value = data.get(key)

        if value is not None:

            cleaned = clean_text(value)

            if cleaned:
                return cleaned

    return ""


# =========================================================
# KEYWORD VARIATIONS
# =========================================================

def get_keyword_variations(keyword):

    keyword = clean_text(keyword).lower()

    if not keyword:
        return []

    variations = set()

    variations.add(keyword)

    if keyword in KEYWORD_ALIASES:

        variations.update(
            KEYWORD_ALIASES[keyword]
        )

    else:

        for main_keyword, aliases in KEYWORD_ALIASES.items():

            if keyword in aliases:

                variations.add(main_keyword)

                variations.update(aliases)

    return list(variations)


# =========================================================
# LOCATION VARIATIONS
# =========================================================

def get_location_variations(location):

    location = clean_text(location).lower()

    if not location:
        return ["remote"]

    if location in LOCATION_ALIASES:

        return LOCATION_ALIASES[location]

    return [
        location,
        "remote"
    ]


# =========================================================
# SEARCH LIVE INTERNSHIPS
# =========================================================

def search_internships(
    keyword,
    location="India"
):

    print()
    print("=" * 70)
    print("LIVE INTERNSHIP SEARCH")
    print("=" * 70)

    print(
        "Keyword:",
        keyword
    )

    print(
        "Location:",
        location
    )

    # -----------------------------------------------------
    # KEYWORD + LOCATION
    # -----------------------------------------------------

    keyword_variations = get_keyword_variations(
        keyword
    )

    location_variations = get_location_variations(
        location
    )

    print(
        "Keyword variations:",
        keyword_variations
    )

    print(
        "Location variations:",
        location_variations
    )

    # -----------------------------------------------------
    # API REQUEST
    # -----------------------------------------------------

    try:

        response = requests.get(
            API_URL,
            headers={
                "User-Agent":
                    "Mozilla/5.0 "
                    "(Windows NT 10.0; Win64; x64)"
            },
            timeout=20
        )

        response.raise_for_status()

        data = response.json()

    except requests.exceptions.RequestException as error:

        print(
            "API connection error:",
            error
        )

        return []

    except ValueError as error:

        print(
            "Invalid API response:",
            error
        )

        return []

    except Exception as error:

        print(
            "Unexpected API error:",
            error
        )

        return []

    # -----------------------------------------------------
    # GET JOB LIST
    # -----------------------------------------------------

    jobs = data.get(
        "data",
        []
    )

    if not isinstance(jobs, list):

        print(
            "Unexpected API data format."
        )

        return []

    print(
        "Jobs received from API:",
        len(jobs)
    )

    # -----------------------------------------------------
    # PROCESS JOBS
    # -----------------------------------------------------

    results = []

    seen_urls = set()

    for job in jobs:

        if not isinstance(job, dict):
            continue

        # -------------------------------------------------
        # EXTRACT FIELDS
        # -------------------------------------------------

        title = get_first_value(
            job,
            [
                "title",
                "job_title",
                "position",
                "role"
            ]
        )

        company = get_first_value(
            job,
            [
                "company_name",
                "company",
                "companyName",
                "employer"
            ]
        )

        job_location = get_first_value(
            job,
            [
                "location",
                "locations",
                "city",
                "place"
            ]
        )

        description = get_first_value(
            job,
            [
                "description",
                "job_description",
                "content"
            ]
        )

        skills = get_first_value(
            job,
            [
                "tags",
                "skills",
                "job_skills"
            ]
        )

        job_type = get_first_value(
            job,
            [
                "job_types",
                "job_type",
                "type"
            ]
        )

        apply_url = get_first_value(
            job,
            [
                "url",
                "apply_url",
                "application_url",
                "link"
            ]
        )

        remote = get_first_value(
            job,
            [
                "remote"
            ]
        )

        # -------------------------------------------------
        # FALLBACK VALUES
        # -------------------------------------------------

        if not title:

            title = "Internship Opportunity"

        if not company:

            company = "Company not specified"

        if not job_location:

            if remote.lower() in [
                "true",
                "yes",
                "1"
            ]:

                job_location = "Remote"

            else:

                job_location = (
                    "Location not specified"
                )

        if not description:

            description = (
                "No description available."
            )

        if not skills:

            skills = "Not specified"

        if not job_type:

            job_type = "Internship"

        if not apply_url:

            apply_url = ""

        # -------------------------------------------------
        # CREATE SEARCH TEXT
        # -------------------------------------------------

        search_text = " ".join(
            [
                title,
                company,
                job_location,
                description,
                skills
            ]
        ).lower()

        # -------------------------------------------------
        # KEYWORD MATCH
        # -------------------------------------------------

        keyword_match = False

        for variation in keyword_variations:

            if variation.lower() in search_text:

                keyword_match = True
                break

        if not keyword_match:

            continue

        # -------------------------------------------------
        # LOCATION MATCH
        # -------------------------------------------------

        location_text = (
            job_location.lower()
        )

        location_match = False

        for location_variation in location_variations:

            if (
                location_variation.lower()
                in location_text
            ):

                location_match = True
                break

        # India is not always explicitly written.
        # If remote is available, accept it.

        if "remote" in location_text:

            location_match = True

        # -------------------------------------------------
        # MATCH SCORE
        # -------------------------------------------------

        score = 0

        # Keyword in title
        title_lower = title.lower()

        for variation in keyword_variations:

            if variation.lower() in title_lower:

                score += 50
                break

        # Keyword somewhere in job
        if keyword_match:

            score += 25

        # Location
        if location_match:

            score += 15

        # Internship
        internship_text = (
            title
            + " "
            + description
        ).lower()

        if (
            "intern" in internship_text
            or "internship" in internship_text
        ):

            score += 10

        if score > 100:

            score = 100

        # -------------------------------------------------
        # DUPLICATE CHECK
        # -------------------------------------------------

        if apply_url:

            if apply_url in seen_urls:

                continue

            seen_urls.add(
                apply_url
            )

        # -------------------------------------------------
        # RESULT
        # -------------------------------------------------

        result = {

            "internship_id":
                job.get(
                    "slug",
                    ""
                ),

            "title":
                title,

            "company":
                company,

            "location":
                job_location,

            "skills":
                skills,

            "eligibility":
                "Check job description",

            "duration":
                "Not specified",

            "stipend":
                "Not specified",

            "description":
                description,

            "apply_url":
                apply_url,

            "type":
                "Internship",

            "job_type":
                job_type,

            "domain":
                "",

            "match_score":
                score,

            "source":
                "Arbeitnow Live API"
        }

        results.append(
            result
        )

    # -----------------------------------------------------
    # SORT RESULTS
    # -----------------------------------------------------

    results.sort(
        key=lambda x:
            x.get(
                "match_score",
                0
            ),
        reverse=True
    )

    print(
        "Matching live internships:",
        len(results)
    )

    print("=" * 70)

    return results


# =========================================================
# DISPLAY LIVE RESULTS
# =========================================================

def display_results(results):

    print()
    print("=" * 70)
    print("LIVE INTERNSHIP RESULTS")
    print("=" * 70)

    if not results:

        print(
            "No matching live internships found."
        )

        return

    for index, item in enumerate(
        results[:10],
        start=1
    ):

        print()
        print(
            f"{index}. "
            f"{item.get('title', 'Unknown')}"
        )

        print(
            "Company:",
            item.get(
                "company",
                "Not specified"
            )
        )

        print(
            "Location:",
            item.get(
                "location",
                "Not specified"
            )
        )

        print(
            "Skills:",
            item.get(
                "skills",
                "Not specified"
            )
        )

        print(
            "Match Score:",
            f"{item.get('match_score', 0)}%"
        )

        print(
            "Apply URL:",
            item.get(
                "apply_url",
                "Not available"
            )
        )

        print("-" * 70)


# =========================================================
# DIRECT TEST
# =========================================================

if __name__ == "__main__":

    print()
    print("=" * 70)
    print("TESTING LIVE INTERNSHIP SEARCH")
    print("=" * 70)

    keyword = input(
        "Enter skill/keyword: "
    ).strip()

    location = input(
        "Enter location: "
    ).strip()

    if not keyword:

        keyword = "Python"

    if not location:

        location = "India"

    results = search_internships(
        keyword,
        location
    )

    display_results(
        results
    )

