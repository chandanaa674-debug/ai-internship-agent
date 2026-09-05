import os
import sys

# ---------------------------------------------------------
# PROJECT ROOT
# ---------------------------------------------------------

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


# ---------------------------------------------------------
# ENVIRONMENT
# ---------------------------------------------------------

try:
    from dotenv import load_dotenv

    load_dotenv(
        os.path.join(
            PROJECT_ROOT,
            ".env"
        )
    )
except ImportError:
    pass


# ---------------------------------------------------------
# PROJECT IMPORTS
# ---------------------------------------------------------

from internship_processor import find_internships

try:
    from agent.prompts import (
        SYSTEM_PROMPT,
        build_user_prompt
    )
except ImportError:

    SYSTEM_PROMPT = """
You are an AI Internship Assistant.
Help students find and understand suitable internships.
"""

    def build_user_prompt(
        keyword,
        location,
        internships
    ):
        return f"""
Find suitable internships for:

Skill: {keyword}
Location: {location}

Internship opportunities:
{internships}
"""


# ---------------------------------------------------------
# GEMINI
# ---------------------------------------------------------

try:
    from google import genai
except ImportError:
    genai = None


GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY"
)


def create_gemini_client():

    if genai is None:
        return None

    if not GEMINI_API_KEY:
        return None

    try:
        return genai.Client(
            api_key=GEMINI_API_KEY
        )
    except Exception as error:
        print(
            f"Gemini client error: {error}"
        )
        return None


# ---------------------------------------------------------
# FALLBACK ANSWER
# ---------------------------------------------------------

def build_fallback_answer(
    keyword,
    location,
    internships
):

    if not internships:
        return (
            f"No internships were found for "
            f"'{keyword}' in '{location}'."
        )

    answer = []

    answer.append(
        f"Found {len(internships)} internship "
        f"opportunities for '{keyword}' "
        f"in '{location}'."
    )

    answer.append("")

    for index, internship in enumerate(
        internships,
        start=1
    ):

        title = internship.get(
            "title",
            "Internship"
        )

        company = internship.get(
            "company",
            "Company not specified"
        )

        job_location = internship.get(
            "location",
            "Location not specified"
        )

        score = internship.get(
            "match_score",
            0
        )

        answer.append(
            f"{index}. {title}"
        )

        answer.append(
            f"   Company: {company}"
        )

        answer.append(
            f"   Location: {job_location}"
        )

        answer.append(
            f"   Match Score: {score}"
        )

        answer.append("")

    return "\n".join(answer)


# ---------------------------------------------------------
# INTERNSHIP AGENT
# ---------------------------------------------------------

class InternshipAgent:

    def __init__(self):

        self.client = create_gemini_client()

        self.models = [
            "gemini-2.5-flash",
            "gemini-2.5-flash-lite"
        ]


    # -----------------------------------------------------
    # SEARCH
    # -----------------------------------------------------

    def search(
        self,
        keyword,
        location="India"
    ):

        try:

            return find_internships(
                keyword,
                location
            )

        except Exception as error:

            print(
                f"Search error: {error}"
            )

            return []


    # -----------------------------------------------------
    # GET TOP MATCHES
    # -----------------------------------------------------

    def get_top_matches(
        self,
        keyword,
        location="India",
        limit=20
    ):

        results = self.search(
            keyword,
            location
        )

        return results[:limit]


    # -----------------------------------------------------
    # ASK AI
    # -----------------------------------------------------

    def ask_ai(
        self,
        keyword,
        location="India",
        limit=20
    ):

        results = self.get_top_matches(
            keyword,
            location,
            limit
        )

        # -----------------------------------------------
        # No results
        # -----------------------------------------------

        if not results:

            return {
                "answer": build_fallback_answer(
                    keyword,
                    location,
                    results
                ),
                "results": [],
                "ai_status": "FALLBACK"
            }


        # -----------------------------------------------
        # Gemini
        # -----------------------------------------------

        if self.client is not None:

            try:

                internships_text = "\n\n".join(
                    str(item)
                    for item in results
                )

                prompt = build_user_prompt(
                    keyword,
                    location,
                    internships_text
                )

                for model in self.models:

                    try:

                        response = (
                            self.client.models.generate_content(
                                model=model,
                                contents=[
                                    SYSTEM_PROMPT,
                                    prompt
                                ]
                            )
                        )

                        answer = getattr(
                            response,
                            "text",
                            None
                        )

                        if answer:

                            return {
                                "answer": answer,
                                "results": results,
                                "ai_status": "GEMINI"
                            }

                    except Exception as error:

                        print(
                            f"Model {model} error: "
                            f"{error}"
                        )

            except Exception as error:

                print(
                    f"Gemini error: {error}"
                )


        # -----------------------------------------------
        # Fallback
        # -----------------------------------------------

        return {
            "answer": build_fallback_answer(
                keyword,
                location,
                results
            ),
            "results": results,
            "ai_status": "FALLBACK"
        }


# ---------------------------------------------------------
# DIRECT TEST
# ---------------------------------------------------------

if __name__ == "__main__":

    print("=" * 70)
    print("INTERNSHIP AGENT")
    print("=" * 70)

    keyword = input(
        "Enter internship skill: "
    ).strip()

    location = input(
        "Enter location: "
    ).strip()

    keyword = keyword or "Python"
    location = location or "Bangalore"

    agent = InternshipAgent()

    result = agent.ask_ai(
        keyword,
        location,
        limit=20
    )

    print()
    print("=" * 70)
    print("INTERNSHIP AGENT RESULT")
    print("=" * 70)

    print(result["answer"])

    print()
    print(
        f"AI Status : {result['ai_status']}"
    )

    print(
        f"Results   : {len(result['results'])}"
    )

    print("=" * 70)
    print("AGENT TEST COMPLETED")
    print("=" * 70)