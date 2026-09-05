import requests
import re


API_URL = "https://www.arbeitnow.com/api/job-board-api"


# =========================================================
# KEYWORD ALIASES
# =========================================================

KEYWORD_ALIASES = {
    "ai": [
        "ai",
        "artificial intelligence",
        "machine learning",
        "ml",
        "aiml",
        "ai/ml",
        "deep learning"
    ],

    "artificial intelligence": [
        "artificial intelligence",
        "ai",
        "machine learning",
        "ml",
        "aiml",
        "ai/ml",
        "deep learning"
    ],

    "machine learning": [
        "machine learning",
        "ml",
        "artificial intelligence",
        "ai",
        "aiml",
        "ai/ml",
        "deep learning"
    ],

    "ml": [
        "machine learning",
        "ml",
        "artificial intelligence",
        "ai",
        "aiml",
        "deep learning"
    ],

    "aiml": [
        "aiml",
        "ai/ml",
        "artificial intelligence",
        "machine learning",
        "ml",
        "deep learning"
    ],

    "data structures": [
        "data structures",
        "data structure",
        "dsa",
        "data structures and algorithms",
        "algorithms"
    ],

    "data structure": [
        "data structure",
        "data structures",
        "dsa",
        "data structures and algorithms",
        "algorithms"
    ],

    "dsa": [
        "dsa",
        "data structures",
        "data structure",
        "algorithms",
        "data structures and algorithms"
    ],

    "python": [
        "python",
        "python programming",
        "python developer"
    ],

    "leadership": [
        "leadership",
        "team leadership",
        "management",
        "team management",
        "project management"
    ]
}


# =========================================================
# LOCATION ALIASES
# =========================================================

LOCATION_ALIASES = {
    "bangalore": [
        "bangalore",
        "bengaluru"
    ],

    "bengaluru": [
        "bangalore",
        "bengaluru"
    ],

    "mangalore": [
        "mangalore",
        "mangaluru"
    ],

    "mangaluru": [
        "mangalore",
        "mangaluru"
    ],

    "mumbai": [
        "mumbai"
    ],

    "delhi": [
        "delhi",
        "new delhi"
    ],

    "hyderabad": [
        "hyderabad"
    ],

    "chennai": [
        "chennai"
    ],

    "pune": [
        "pune"
    ],

    "india": [
        "india"
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

def clean_html(text):

    if text is None:
        return ""

    text = str(text)

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
# KEYWORD VARIATIONS
# =========================================================

def get_keyword_variations(keyword):

    keyword = str(
        keyword or ""
    ).lower().strip()

    return KEYWORD_ALIASES.get(
        keyword,
        [keyword]
    )


# =========================================================
# LOCATION VARIATIONS
# =========================================================

def get_location_variations(location):

    location = str(
        location or ""
    ).lower().strip()

    return LOCATION_ALIASES.get(
        location,
        [location]
    )


# =========================================================
# SEARCH INTERNSHIPS
# =========================================================

def search_internships(
    keyword,
    location="India"
):

    try:

        keyword = str(
            keyword or ""
        ).lower().strip()

        location = str(
            location or "India"
        ).lower().strip()

        if not keyword:
            print("Please enter a keyword.")
            return []

        print()
        print("=" * 70)
        print("SEARCHING INTERNSHIPS")
        print("=" * 70)
        print("Keyword :", keyword)
        print("Location:", location)
        print("=" * 70)

        # -------------------------------------------------
        # GET DATA FROM API
        # -------------------------------------------------

        response = requests.get(
            API_URL,
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

        jobs = data.get(
            "data",
            []
        )

        if not isinstance(jobs, list):
            jobs = []

        print(
            "Jobs received from API:",
            len(jobs)
        )

        # -------------------------------------------------
        # KEYWORD VARIATIONS
        # -------------------------------------------------

        keyword_variations = (
            get_keyword_variations(
                keyword
            )
        )

        # -------------------------------------------------
        # LOCATION VARIATIONS
        # -------------------------------------------------

        location_variations = (
            get_location_variations(
                location
            )
        )

        results = []

        # -------------------------------------------------
        # PROCESS JOBS
        # -------------------------------------------------

        for job in jobs:

            if not isinstance(
                job,
                dict
            ):
                continue

            title = clean_html(
                job.get(
                    "title",
                    ""
                )
            )

            company = clean_html(
                job.get(
                    "company_name",
                    job.get(
                        "company",
                        "Not specified"
                    )
                )
            )

            job_location = clean_html(
                job.get(
                    "location",
                    ""
                )
            )

            description = clean_html(
                job.get(
                    "description",
                    ""
                )
            )

            tags = job.get(
                "tags",
                []
            )

            if isinstance(
                tags,
                list
            ):

                tags_text = ", ".join(
                    str(tag)
                    for tag in tags
                    if tag
                )

            else:

                tags_text = str(
                    tags or ""
                )

            tags_text = clean_html(
                tags_text
            )

            # -------------------------------------------------
            # SEARCHABLE TEXT
            # -------------------------------------------------

            searchable = (
                title + " " +
                company + " " +
                job_location + " " +
                tags_text + " " +
                description
            ).lower()

            # -------------------------------------------------
            # KEYWORD MATCH
            # -------------------------------------------------

            keyword_match = False

            for variation in keyword_variations:

                variation = (
                    str(variation)
                    .lower()
                    .strip()
                )

                if variation and variation in searchable:

                    keyword_match = True
                    break

            if not keyword_match:
                continue

            # -------------------------------------------------
            # INTERNSHIP CHECK
            # -------------------------------------------------

            job_type = str(
                job.get(
                    "job_type",
                    ""
                )
            ).lower()

            employment_type = str(
                job.get(
                    "employment_type",
                    ""
                )
            ).lower()

            internship_text = (
                searchable + " " +
                job_type + " " +
                employment_type
            )

            internship_words = [
                "intern",
                "internship",
                "trainee"
            ]

            is_internship = any(
                word in internship_text
                for word in internship_words
            )

            # If the API does not explicitly say
            # internship, still keep the relevant result.
            # This prevents valid opportunities from
            # disappearing.

            # -------------------------------------------------
            # LOCATION CHECK
            # -------------------------------------------------

            location_match = False

            location_text = (
                job_location + " " +
                description + " " +
                title
            ).lower()

            if location in [
                "india",
                "all",
                "any",
                "worldwide"
            ]:

                location_match = True

            else:

                for location_name in location_variations:

                    if (
                        location_name.lower()
                        in location_text
                    ):

                        location_match = True
                        break

                # Remote opportunities are also acceptable
                if "remote" in location_text:

                    location_match = True

            # If location is missing from the API,
            # keep the relevant internship instead
            # of returning zero results.

            if not location_match:

                if not job_location:

                    location_match = True

            # -------------------------------------------------
            # SCORE
            # -------------------------------------------------

            match_score = 0

            title_lower = title.lower()
            tags_lower = tags_text.lower()
            description_lower = description.lower()

            for variation in keyword_variations:

                variation = (
                    str(variation)
                    .lower()
                    .strip()
                )

                if variation in title_lower:
                    match_score += 50

                if variation in tags_lower:
                    match_score += 30

                if variation in description_lower:
                    match_score += 10

            if location_match:
                match_score += 20

            if is_internship:
                match_score += 20

            # -------------------------------------------------
            # APPLY URL
            # -------------------------------------------------

            apply_url = (
                job.get("url")
                or job.get("apply_url")
                or job.get("application_url")
                or ""
            )

            apply_url = str(
                apply_url
            ).strip()

            # -------------------------------------------------
            # CREATE RESULT
            # -------------------------------------------------

            results.append({

                "title":
                    title
                    or "Internship Opportunity",

                "company":
                    company
                    or "Not specified",

                "location":
                    job_location
                    or "Remote / Not specified",

                "skills":
                    tags_text
                    or "Not specified",

                "eligibility":
                    "Check job description",

                "duration":
                    "Not specified",

                "stipend":
                    "Not specified",

                "description":
                    description
                    or "No description available.",

                "apply_url":
                    apply_url,

                "type":
                    "Internship",

                "match_score":
                    match_score
            })

        # -------------------------------------------------
        # REMOVE DUPLICATES
        # -------------------------------------------------

        unique_results = []

        seen = set()

        for item in results:

            key = (
                item["title"].lower().strip(),
                item["company"].lower().strip(),
                item["apply_url"].lower().strip()
            )

            if key not in seen:

                seen.add(key)

                unique_results.append(
                    item
                )

        # -------------------------------------------------
        # SORT BY SCORE
        # -------------------------------------------------

        unique_results.sort(
            key=lambda item:
            item.get(
                "match_score",
                0
            ),
            reverse=True
        )

        print(
            "Matching internships:",
            len(unique_results)
        )

        print("=" * 70)

        return unique_results

    # -----------------------------------------------------
    # API ERROR
    # -----------------------------------------------------

    except requests.exceptions.RequestException as error:

        print()
        print("API CONNECTION ERROR:")
        print(error)
        print()

        return []

    # -----------------------------------------------------
    # JSON ERROR
    # -----------------------------------------------------

    except ValueError as error:

        print()
        print("API RESPONSE ERROR:")
        print(error)
        print()

        return []

    # -----------------------------------------------------
    # OTHER ERROR
    # -----------------------------------------------------

    except Exception as error:

        print()
        print("SEARCH ERROR:")
        print(error)
        print()

        return []


# =========================================================
# TEST DIRECTLY
# =========================================================

if __name__ == "__main__":

    keyword = input(
        "Enter internship skill: "
    ).strip()

    location = input(
        "Enter location: "
    ).strip()

    results = search_internships(
        keyword,
        location
    )

    print()
    print("=" * 70)
    print("RESULTS")
    print("=" * 70)

    if not results:

        print(
            "No matching internships found."
        )

    else:

        for index, item in enumerate(
            results,
            start=1
        ):

            print()
            print(
                f"{index}. {item['title']}"
            )

            print(
                "Company:",
                item["company"]
            )

            print(
                "Location:",
                item["location"]
            )

            print(
                "Skills:",
                item["skills"]
            )

            print(
                "Eligibility:",
                item["eligibility"]
            )

            print(
                "Duration:",
                item["duration"]
            )

            print(
                "Stipend:",
                item["stipend"]
            )

            print(
                "Apply URL:",
                item["apply_url"]
            )

            print(
                "Score:",
                item["match_score"]
            )

            print("-" * 70)