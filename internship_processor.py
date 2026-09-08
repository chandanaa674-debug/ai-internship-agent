import csv
import os

from internship_search import search_internships
from internship_ranker import rank_internships


# =========================================================
# LOAD KAGGLE DATASET
# =========================================================

def load_dataset():

    file_path = os.path.join(
        "data",
        "internship_agent_dataset.csv"
    )

    if not os.path.exists(file_path):

        print("ERROR: Dataset file not found!")
        print("Expected:")
        print(file_path)

        return []

    internships = []

    try:

        with open(
            file_path,
            "r",
            encoding="utf-8-sig",
            newline=""
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:

                title = str(
                    row.get("title", "")
                ).strip()

                if not title:
                    continue

                internship = {

                    "internship_id":
                        row.get(
                            "internship_id",
                            ""
                        ),

                    "title":
                        title,

                    "company":
                        row.get(
                            "company",
                            ""
                        ),

                    "location":
                        row.get(
                            "location",
                            ""
                        ),

                    "description":
                        row.get(
                            "description",
                            ""
                        ),

                    "skills":
                        row.get(
                            "skills",
                            ""
                        ),

                    "domain":
                        row.get(
                            "domain",
                            ""
                        ),

                    "job_type":
                        row.get(
                            "job_type",
                            ""
                        ),

                    "apply_url":
                        row.get(
                            "apply_url",
                            ""
                        ),

                    "source":
                        "Kaggle"
                }

                internships.append(internship)

        print(
            f"Kaggle records loaded: "
            f"{len(internships)}"
        )

        return internships

    except Exception as e:

        print(
            "Error loading dataset:",
            e
        )

        return []


# =========================================================
# CONVERT LIVE API RESULT
# =========================================================

def prepare_live_result(item):

    return {

        "internship_id":
            item.get(
                "internship_id",
                ""
            ),

        "title":
            item.get(
                "title",
                "Internship Opportunity"
            ),

        "company":
            item.get(
                "company",
                "Company not specified"
            ),

        "location":
            item.get(
                "location",
                "Location not specified"
            ),

        "description":
            item.get(
                "description",
                "No description available."
            ),

        "skills":
            item.get(
                "skills",
                "Not specified"
            ),

        "domain":
            item.get(
                "domain",
                ""
            ),

        "job_type":
            item.get(
                "job_type",
                "Internship"
            ),

        "apply_url":
            item.get(
                "apply_url",
                ""
            ),

        "source":
            item.get(
                "source",
                "Live API"
            ),

        "duration":
            item.get(
                "duration",
                "Not specified"
            ),

        "stipend":
            item.get(
                "stipend",
                "Not specified"
            )
    }


# =========================================================
# REMOVE DUPLICATES
# =========================================================

def remove_duplicates(internships):

    unique = []

    seen = set()

    for item in internships:

        title = str(
            item.get(
                "title",
                ""
            )
        ).strip().lower()

        company = str(
            item.get(
                "company",
                ""
            )
        ).strip().lower()

        location = str(
            item.get(
                "location",
                ""
            )
        ).strip().lower()

        key = (
            title,
            company,
            location
        )

        if key in seen:
            continue

        seen.add(key)

        unique.append(item)

    return unique


# =========================================================
# MAIN SEARCH FUNCTION
# =========================================================

def find_internships(

    keyword,

    location="India",

    user_skills="",

    user_domain="",

    user_role="",

    user_query="",

    include_live=True,

    user_interests=None
):

    print("\n======================================")
    print("      AI INTERNSHIP RECOMMENDER")
    print("======================================")

    # Make sure interests is always a list
    if user_interests is None:
        user_interests = []


    # =====================================================
    # 1. LOAD KAGGLE DATA
    # =====================================================

    dataset_results = load_dataset()


    # =====================================================
    # 2. SEARCH LIVE INTERNSHIPS
    # =====================================================

    live_results = []

    if include_live:

        print("\n======================================")
        print("      FETCHING LIVE INTERNSHIPS")
        print("======================================")

        try:

            live_results = search_internships(
                keyword,
                location
            )

            if live_results is None:
                live_results = []

            print(
                "Live internships found:",
                len(live_results)
            )

        except Exception as e:

            print(
                "Live API search failed:",
                e
            )

            live_results = []


    # =====================================================
    # 3. CONVERT LIVE RESULTS
    # =====================================================

    processed_live = []

    for item in live_results:

        try:

            processed_item = prepare_live_result(
                item
            )

            processed_live.append(
                processed_item
            )

        except Exception as e:

            print(
                "Error processing live result:",
                e
            )


    # =====================================================
    # 4. COMBINE KAGGLE + LIVE
    # =====================================================

    combined = []

    combined.extend(
        dataset_results
    )

    combined.extend(
        processed_live
    )


    print("\n======================================")
    print("          COMBINING RESULTS")
    print("======================================")

    print(
        "Kaggle results:",
        len(dataset_results)
    )

    print(
        "Live results:",
        len(processed_live)
    )

    print(
        "Total before duplicate removal:",
        len(combined)
    )


    # =====================================================
    # 5. REMOVE DUPLICATES
    # =====================================================

    combined = remove_duplicates(
        combined
    )

    print(
        "Total after duplicate removal:",
        len(combined)
    )


    # =====================================================
    # 6. RANK INTERNSHIPS
    # =====================================================

    print("\n======================================")
    print("          RANKING INTERNSHIPS")
    print("======================================")


    try:

        ranked = rank_internships(

            combined,

            user_skills=user_skills,

            user_domain=user_domain,

            user_role=user_role,

            user_query=user_query,

            user_interests=user_interests
        )

    except Exception as e:

        print(
            "Ranking error:",
            e
        )

        # Do not destroy search results
        ranked = combined


    return ranked


# =========================================================
# DISPLAY RESULTS
# =========================================================

def display_results(results):

    print("\n======================================")
    print("       TOP INTERNSHIP RECOMMENDATIONS")
    print("======================================")


    if not results:

        print(
            "\nNo internships found."
        )

        return


    for index, item in enumerate(
        results[:10],
        start=1
    ):

        print("\n--------------------------------------")

        print(
            f"{index}. "
            f"{item.get('title', 'N/A')}"
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
            "Domain:",
            item.get(
                "domain",
                "Not specified"
            )
        )

        print(
            "Job Type:",
            item.get(
                "job_type",
                "Not specified"
            )
        )

        print(
            "Source:",
            item.get(
                "source",
                "Unknown"
            )
        )

        print(
            "Match Score:",
            item.get(
                "match_score",
                0
            )
        )

        print(
            "Apply URL:",
            item.get(
                "apply_url",
                "Not available"
            )
        )


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    keyword = input(
        "Enter internship keyword: "
    ).strip()

    location = input(
        "Enter preferred location: "
    ).strip()

    user_skills = input(
        "Enter your skills: "
    ).strip()

    user_domain = input(
        "Enter your domain: "
    ).strip()

    user_role = input(
        "Enter preferred role: "
    ).strip()

    user_query = input(
        "Enter your internship query: "
    ).strip()


    results = find_internships(

        keyword=keyword,

        location=location,

        user_skills=user_skills,

        user_domain=user_domain,

        user_role=user_role,

        user_query=user_query,

        include_live=True,

        user_interests=[]
    )


    display_results(results)