import os
import sys
import time

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
    You are an AI Internship Recommendation Agent.

    Help students find suitable internships based on
    their skills, domain, preferred role, location,
    projects and requirements.

    Give clear and useful recommendations.
    """

    def build_user_prompt(
        keyword,
        location,
        internships,
        student_profile=None
    ):

        return f"""
        Find suitable internships for:

        Keyword: {keyword}
        Location: {location}

        Student Profile:
        {student_profile}

        Internship Opportunities:
        {internships}

        Recommend the most suitable internships.
        Explain why they are suitable.
        """


# ---------------------------------------------------------
# GEMINI
# ---------------------------------------------------------

try:
    from google import genai
except ImportError:
    genai = None


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


def create_gemini_client():

    if genai is None:

        print("Gemini package is not installed.")

        return None

    if not GEMINI_API_KEY:

        print("GEMINI_API_KEY was not found.")

        return None

    try:

        client = genai.Client(
            api_key=GEMINI_API_KEY
        )

        print(
            "Gemini client created successfully."
        )

        return client

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
        internships[:10],
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

        skills = internship.get(
            "skills",
            "Not specified"
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
            f"   Skills: {skills}"
        )

        answer.append(
            f"   Match Score: {score}%"
        )

        answer.append("")

    return "\n".join(answer)


# ---------------------------------------------------------
# INTERNSHIP AGENT
# ---------------------------------------------------------

class InternshipAgent:

    def __init__(self):

        self.client = create_gemini_client()

        # Current Gemini models
        self.models = [
            "gemini-3.7-flash",
            "gemini-3.8-flash"
        ]


    # -----------------------------------------------------
    # SEARCH
    # -----------------------------------------------------

    def search(
        self,
        keyword,
        location="India",
        user_skills="",
        user_domain="",
        user_role="",
        user_query=""
    ):

        try:

            return find_internships(
                keyword=keyword,
                location=location,
                user_skills=user_skills,
                user_domain=user_domain,
                user_role=user_role,
                user_query=user_query,
                include_live=True
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
        user_skills="",
        user_domain="",
        user_role="",
        user_query="",
        limit=20
    ):

        results = self.search(
            keyword=keyword,
            location=location,
            user_skills=user_skills,
            user_domain=user_domain,
            user_role=user_role,
            user_query=user_query
        )

        return results[:limit]


    # -----------------------------------------------------
    # ASK GEMINI
    # -----------------------------------------------------

    def ask_ai(
        self,
        keyword,
        location="India",
        user_skills="",
        user_domain="",
        user_role="",
        user_query="",
        student_profile=None,
        limit=20,
        internships=None
    ):

        # IMPORTANT:
        # If Flask already searched internships,
        # use those results instead of searching again.

        if internships is not None:

            results = internships[:limit]

        else:

            results = self.get_top_matches(
                keyword=keyword,
                location=location,
                user_skills=user_skills,
                user_domain=user_domain,
                user_role=user_role,
                user_query=user_query,
                limit=limit
            )


        # -------------------------------------------------
        # NO RESULTS
        # -------------------------------------------------

        if not results:

            return {
                "answer": build_fallback_answer(
                    keyword,
                    location,
                    results
                ),
                "results": [],
                "ai_status": "NO_RESULTS"
            }


        # -------------------------------------------------
        # GEMINI NOT AVAILABLE
        # -------------------------------------------------

        if self.client is None:

            print(
                "Gemini is unavailable. "
                "Using fallback recommendation."
            )

            return {
                "answer": build_fallback_answer(
                    keyword,
                    location,
                    results
                ),
                "results": results,
                "ai_status": "FALLBACK"
            }


        # -------------------------------------------------
        # BUILD PROMPT
        # -------------------------------------------------

        try:

            prompt = build_user_prompt(
                keyword=keyword,
                location=location,
                internships=results,
                student_profile=student_profile
            )

        except Exception as error:

            print(
                f"Prompt creation error: {error}"
            )

            return {
                "answer": build_fallback_answer(
                    keyword,
                    location,
                    results
                ),
                "results": results,
                "ai_status": "FALLBACK"
            }


        # -------------------------------------------------
        # TRY GEMINI
        # -------------------------------------------------

        for model in self.models:

            print(
                f"Trying Gemini model: {model}"
            )

            for attempt in range(2):

                try:

                    response = (
                        self.client.models.generate_content(
                            model=model,
                            contents=prompt
                        )
                    )

                    answer = getattr(
                        response,
                        "text",
                        None
                    )

                    if answer:

                        print(
                            f"Gemini response received "
                            f"from {model}"
                        )

                        return {
                            "answer": answer,
                            "results": results,
                            "ai_status": "GEMINI"
                        }

                    print(
                        f"{model} returned empty response."
                    )

                except Exception as error:

                    error_text = str(error)

                    print(
                        f"{model} attempt "
                        f"{attempt + 1} failed:"
                    )

                    print(error_text)


                    if (
                        "503" in error_text
                        or "429" in error_text
                        or "500" in error_text
                    ):

                        if attempt == 0:

                            print(
                                "Retrying after 3 seconds..."
                            )

                            time.sleep(3)

                            continue

                    break


        # -------------------------------------------------
        # FINAL FALLBACK
        # -------------------------------------------------

        print(
            "All Gemini attempts failed. "
            "Using fallback recommendation."
        )

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

    print(
        "INTERNSHIP AGENT TEST"
    )

    print("=" * 70)

    keyword = input(
        "Enter internship skill: "
    ).strip()

    location = input(
        "Enter location: "
    ).strip()

    keyword = keyword or "Python"

    location = location or "Bangalore"


    student_profile = {

        "full_name": "Student",

        "year": "3rd Year",

        "college": "Example College",

        "degree": "B.Tech Computer Science",

        "skills": (
            "Python, SQL, Flask, Machine Learning"
        ),

        "preferred_role": (
            "Python Developer"
        ),

        "work_preference": "Remote",

        "projects": (
            "Built a Flask AI internship "
            "recommendation project."
        )
    }


    agent = InternshipAgent()


    result = agent.ask_ai(

        keyword=keyword,

        location=location,

        user_skills=student_profile["skills"],

        user_domain=student_profile["degree"],

        user_role=student_profile["preferred_role"],

        user_query=student_profile["projects"],

        student_profile=student_profile,

        limit=20
    )


    print()

    print("=" * 70)

    print(
        "INTERNSHIP AGENT RESULT"
    )

    print("=" * 70)

    print(
        result["answer"]
    )

    print()

    print(
        f"AI Status : {result['ai_status']}"
    )

    print(
        f"Results   : {len(result['results'])}"
    )

    print("=" * 70)

    print(
        "TEST COMPLETED"
    )

    print("=" * 70)