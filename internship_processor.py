
"""
Internship Processor
--------------------

Pipeline:

LIVE SEARCH
    ↓
DETAIL PROCESSING
    ↓
RANKING
    ↓
ALL RESULTS RETURNED
"""

from typing import Any, Dict, List

from internship_search import search_internships
from internship_details import process_all_details
from internship_ranker import rank_internships


# ============================================================
# FIND INTERNSHIPS
# ============================================================

def find_internships(
    keyword: str,
    location: str = "India"
) -> List[Dict[str, Any]]:
    """
    Complete internship processing pipeline.

    No result limit is applied here.

    Returns every matching internship obtained from the
    live search source.
    """

    keyword = str(
        keyword or ""
    ).strip()

    location = str(
        location or "India"
    ).strip()

    if not keyword:
        return []

    print()
    print("=" * 70)
    print("INTERNSHIP PROCESSOR")
    print("=" * 70)

    # ========================================================
    # STEP 1 — LIVE SEARCH
    # ========================================================

    print("STEP 1: Searching live internship source...")

    raw_results = search_internships(
        keyword=keyword,
        location=location
    )

    print(
        f"STEP 1 COMPLETE: "
        f"{len(raw_results)} internships found."
    )

    if not raw_results:
        print(
            "No internships found."
        )

        return []

    # ========================================================
    # STEP 2 — PROCESS DETAILS
    # ========================================================

    print()
    print(
        "STEP 2: Processing internship details..."
    )

    try:

        processed_results = process_all_details(
            raw_results
        )

    except Exception as error:

        print(
            f"WARNING: Detail processing failed: "
            f"{error}"
        )

        # Keep original data rather than losing all
        # internship results.
        processed_results = raw_results

    print(
        f"STEP 2 COMPLETE: "
        f"{len(processed_results)} internships processed."
    )

    # ========================================================
    # STEP 3 — RANK
    # ========================================================

    print()
    print(
        "STEP 3: Ranking internship matches..."
    )

    try:

        ranked_results = rank_internships(
            processed_results,
            keyword,
            location
        )

    except Exception as error:

        print(
            f"WARNING: Ranking failed: "
            f"{error}"
        )

        # If ranking fails, still return all internships.
        ranked_results = processed_results

    # ========================================================
    # IMPORTANT
    # ========================================================
    #
    # DO NOT use:
    #
    # ranked_results[:5]
    # ranked_results[:10]
    # ranked_results[:20]
    #
    # We return ALL results.
    # ========================================================

    print(
        f"STEP 3 COMPLETE: "
        f"{len(ranked_results)} internships available."
    )

    print()
    print("=" * 70)
    print(
        f"FINAL RESULTS: {len(ranked_results)}"
    )
    print("=" * 70)
    print()

    return ranked_results


# ============================================================
# DIRECT TEST
# ============================================================

if __name__ == "__main__":

    keyword = input(
        "Enter internship skill: "
    ).strip()

    location = input(
        "Enter location: "
    ).strip()

    if not location:
        location = "India"

    results = find_internships(
        keyword=keyword,
        location=location
    )

    print()

    print(
        f"TOTAL INTERNSHIPS: {len(results)}"
    )

    print()

    for index, internship in enumerate(
        results,
        start=1
    ):

        print("-" * 70)

        print(
            f"{index}. "
            f"{internship.get('title', 'N/A')}"
        )

        print(
            f"Company: "
            f"{internship.get('company', 'N/A')}"
        )

        print(
            f"Location: "
            f"{internship.get('location', 'N/A')}"
        )

        print(
            f"Match Score: "
            f"{internship.get('match_score', 0)}"
        )

        print(
            f"Apply URL: "
            f"{internship.get('apply_url', 'N/A')}"
        )

