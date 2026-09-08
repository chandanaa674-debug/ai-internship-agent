# ============================================================
# internship_rank.py
# AI Internship Recommendation + Personalized Ranking
# ============================================================

import re


# ============================================================
# TEXT HELPERS
# ============================================================

def normalize(value):
    """
    Convert text/list values into lowercase searchable text.
    """

    if isinstance(value, list):
        return " ".join(
            str(item) for item in value
        ).lower()

    return str(value or "").lower()


def words(text):
    """
    Extract searchable words/tokens.
    """

    return set(
        re.findall(
            r"[a-zA-Z0-9+#.]+",
            normalize(text)
        )
    )


# ============================================================
# EXISTING PROFILE MATCHING
# ============================================================

def calculate_match_score(
    internship,
    user_skills="",
    user_domain="",
    user_role="",
    user_query=""
):
    """
    Calculate the original internship match score.

    Score:
        Skills       = 50
        Domain       = 20
        Role/Title   = 15
        Description  = 10
        Job Type     = 5

    Maximum = 100
    """

    score = 0

    # --------------------------------------------------------
    # Internship information
    # --------------------------------------------------------

    internship_skills = normalize(
        internship.get("skills", "")
    )

    title = normalize(
        internship.get("title", "")
    )

    description = normalize(
        internship.get("description", "")
    )

    domain = normalize(
        internship.get("domain", "")
    )

    job_type = normalize(
        internship.get("job_type", "")
    )

    # ========================================================
    # 1. SKILLS — 50 POINTS
    # ========================================================

    requested_skills = words(user_skills)

    if requested_skills:

        matched_skills = 0

        for skill in requested_skills:

            if skill in internship_skills:
                matched_skills += 1

            elif skill in title:
                matched_skills += 1

            elif skill in description:
                matched_skills += 1

        skill_score = (
            matched_skills /
            len(requested_skills)
        ) * 50

        score += skill_score

    # ========================================================
    # 2. DOMAIN — 20 POINTS
    # ========================================================

    if user_domain:

        domain_text = normalize(
            user_domain
        )

        if domain_text in domain:
            score += 20

        elif domain_text in title:
            score += 15

        elif domain_text in description:
            score += 10

    # ========================================================
    # 3. ROLE / TITLE — 15 POINTS
    # ========================================================

    if user_role:

        role_words = words(
            user_role
        )

        title_words = words(
            title
        )

        if role_words:

            matched_role_words = len(
                role_words.intersection(
                    title_words
                )
            )

            score += (
                matched_role_words /
                len(role_words)
            ) * 15

    # ========================================================
    # 4. DESCRIPTION / QUERY — 10 POINTS
    # ========================================================

    if user_query:

        query_words = words(
            user_query
        )

        description_words = words(
            description
        )

        if query_words:

            matched_query_words = len(
                query_words.intersection(
                    description_words
                )
            )

            score += (
                matched_query_words /
                len(query_words)
            ) * 10

    # ========================================================
    # 5. JOB TYPE — 5 POINTS
    # ========================================================

    if "intern" in job_type:

        score += 5

    # ========================================================
    # FINAL SCORE
    # ========================================================

    return min(
        100,
        round(score, 2)
    )


# ============================================================
# LEARNED USER INTEREST SCORE
# ============================================================

def calculate_interest_score(
    internship,
    user_interests
):
    """
    Calculate how strongly an internship matches
    the user's previously learned interests.

    Example:

        User frequently views:
            Python
            AI
            Machine Learning

        Internship containing those interests
        receives a higher behavioral score.
    """

    if not user_interests:
        return 0

    # --------------------------------------------------------
    # Combine internship information into searchable text
    # --------------------------------------------------------

    text = " ".join([
        str(
            internship.get(
                "title",
                ""
            )
        ),

        str(
            internship.get(
                "company",
                ""
            )
        ),

        str(
            internship.get(
                "description",
                ""
            )
        ),

        str(
            internship.get(
                "skills",
                ""
            )
        ),

        str(
            internship.get(
                "domain",
                ""
            )
        ),

        str(
            internship.get(
                "job_type",
                ""
            )
        )
    ]).lower()

    # --------------------------------------------------------
    # Calculate weighted interest match
    # --------------------------------------------------------

    matched_interest_score = 0

    total_interest_score = 0

    for item in user_interests:

        # Database returns dictionaries:
        #
        # {
        #     "interest": "python",
        #     "score": 12
        # }

        if isinstance(
            item,
            dict
        ):

            interest = str(
                item.get(
                    "interest",
                    ""
                )
            ).lower()

            try:
                interest_weight = int(
                    item.get(
                        "score",
                        0
                    )
                )
            except (
                ValueError,
                TypeError
            ):
                interest_weight = 0

        else:

            # Also support simple strings
            interest = str(
                item
            ).lower()

            interest_weight = 1

        # Ignore empty interests

        if not interest:
            continue

        if interest_weight <= 0:
            continue

        total_interest_score += (
            interest_weight
        )

        # ----------------------------------------------------
        # Check whether interest appears in internship
        # ----------------------------------------------------

        if interest in text:

            matched_interest_score += (
                interest_weight
            )

    # --------------------------------------------------------
    # Prevent division by zero
    # --------------------------------------------------------

    if total_interest_score == 0:
        return 0

    # --------------------------------------------------------
    # Convert to 0–100
    # --------------------------------------------------------

    interest_score = (
        matched_interest_score /
        total_interest_score
    ) * 100

    return min(
        100,
        round(interest_score, 2)
    )


# ============================================================
# FINAL PERSONALIZED RANKING
# ============================================================

def rank_internships(
    internships,
    user_skills="",
    user_domain="",
    user_role="",
    user_query="",
    user_interests=None
):
    """
    Rank internships using two systems:

    1. Existing profile matching
    2. Learned behavioral interests

    Existing profile matching:
        75%

    Learned interests:
        25%

    If the user has no learned interests,
    the original score is used.
    """

    ranked = []

    # --------------------------------------------------------
    # Make sure interests is a list
    # --------------------------------------------------------

    if user_interests is None:
        user_interests = []

    # ========================================================
    # PROCESS EVERY INTERNSHIP
    # ========================================================

    for internship in internships:

        # ----------------------------------------------------
        # EXISTING MATCH SCORE
        # ----------------------------------------------------

        base_score = calculate_match_score(
            internship,

            user_skills=user_skills,

            user_domain=user_domain,

            user_role=user_role,

            user_query=user_query
        )

        # ----------------------------------------------------
        # LEARNED INTEREST SCORE
        # ----------------------------------------------------

        interest_score = calculate_interest_score(
            internship,

            user_interests
        )

        # ====================================================
        # COMBINE BOTH SCORES
        # ====================================================

        if user_interests:

            final_score = (
                base_score * 0.75
            ) + (
                interest_score * 0.25
            )

        else:

            final_score = base_score

        # ----------------------------------------------------
        # Copy internship so original data is not modified
        # ----------------------------------------------------

        item = internship.copy()

        # ----------------------------------------------------
        # Store individual scores
        # ----------------------------------------------------

        item[
            "base_match_score"
        ] = round(
            base_score
        )

        item[
            "interest_score"
        ] = round(
            interest_score
        )

        # ----------------------------------------------------
        # Final personalized score
        # ----------------------------------------------------

        item[
            "match_score"
        ] = round(
            final_score
        )

        # ----------------------------------------------------
        # Add to ranking list
        # ----------------------------------------------------

        ranked.append(
            item
        )

    # ========================================================
    # SORT HIGHEST MATCH FIRST
    # ========================================================

    ranked.sort(
        key=lambda x: x.get(
            "match_score",
            0
        ),
        reverse=True
    )

    return ranked


# ============================================================
# GET TOP INTERNSHIPS
# ============================================================

def get_top_internships(
    internships,
    limit=10
):
    """
    Return only the top N internships.
    """

    return internships[:limit]


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    sample_internships = [

        {
            "title": "Python Developer Intern",

            "company": "Example Company",

            "location": "Bangalore",

            "skills": [
                "Python",
                "Flask",
                "SQL"
            ],

            "description":
                "Work on Python backend applications.",

            "domain":
                "Software Development",

            "job_type":
                "Internship"
        },

        {
            "title": "Java Developer Intern",

            "company": "Another Company",

            "location": "Mumbai",

            "skills": [
                "Java",
                "Spring"
            ],

            "description":
                "Develop Java applications.",

            "domain":
                "Software Development",

            "job_type":
                "Internship"
        }
    ]

    # Simulated learned interests

    learned_interests = [

        {
            "interest": "python",
            "score": 15
        },

        {
            "interest": "flask",
            "score": 8
        },

        {
            "interest": "sql",
            "score": 5
        }
    ]

    results = rank_internships(

        sample_internships,

        user_skills="Python SQL",

        user_domain="Software Development",

        user_role="Python Developer",

        user_query="Python internship",

        user_interests=learned_interests
    )

    print("\n====================================")
    print("PERSONALIZED INTERNSHIP RANKING")
    print("====================================\n")

    for internship in results:

        print(
            internship["title"],
            "->",
            internship["match_score"],
            "%"
        )

        print(
            "Base:",
            internship["base_match_score"]
        )

        print(
            "Interest:",
            internship["interest_score"]
        )

        print()