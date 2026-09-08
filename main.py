from flask import Flask, render_template, request, jsonify

from internship_processor import find_internships

from internship_db import (
    initialize_database,
    record_interaction,
    get_user_interests
)

from agent.agent import InternshipAgent


app = Flask(__name__)


# =========================================================
# INITIALIZE DATABASE
# =========================================================

initialize_database()


# =========================================================
# INITIALIZE AI AGENT
# =========================================================

try:

    ai_agent = InternshipAgent()

    print("AI Agent initialized successfully.")

except Exception as error:

    ai_agent = None

    print(
        "AI Agent initialization failed:",
        error
    )


# =========================================================
# HOME PAGE
# =========================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# =========================================================
# SEARCH INTERNSHIPS
# =========================================================

@app.route("/search", methods=["POST"])
def search():

    try:

        data = request.get_json() or {}


        # -------------------------------------------------
        # USER INFORMATION
        # -------------------------------------------------

        user_id = data.get(
            "user_id",
            data.get(
                "email",
                "guest"
            )
        )


        # -------------------------------------------------
        # SEARCH INFORMATION
        # -------------------------------------------------

        keyword = str(
            data.get(
                "keyword",
                ""
            )
        ).strip()

        location = str(
            data.get(
                "location",
                "India"
            )
        ).strip()

        skills = data.get(
            "skills",
            ""
        )

        domain = data.get(
            "domain",
            ""
        )

        role = data.get(
            "role",
            ""
        )

        query = data.get(
            "query",
            ""
        )


        # -------------------------------------------------
        # VALIDATE SEARCH
        # -------------------------------------------------

        if not keyword:

            return jsonify({

                "success": False,

                "message":
                    "Please enter an internship role or skill."

            }), 400


        # -------------------------------------------------
        # RECORD SEARCH BEHAVIOR
        # -------------------------------------------------

        record_interaction(

            user_id=user_id,

            action="search",

            role=role,

            location=location,

            skills=skills,

            search_keyword=keyword

        )


        # -------------------------------------------------
        # GET LEARNED USER INTERESTS
        # -------------------------------------------------

        learned_interests = get_user_interests(
            user_id
        )


        print("\nUser:", user_id)

        print(
            "Learned interests:",
            learned_interests
        )


        # -------------------------------------------------
        # FIND INTERNSHIPS
        # -------------------------------------------------

        results = find_internships(

            keyword=keyword,

            location=location,

            user_skills=skills,

            user_domain=domain,

            user_role=role,

            user_query=query,

            include_live=True,

            user_interests=learned_interests

        )


        # -------------------------------------------------
        # LIMIT RESULTS
        # -------------------------------------------------

        results = results[:20]


        # -------------------------------------------------
        # AI RECOMMENDATION
        # -------------------------------------------------

        ai_answer = ""

        ai_status = "unavailable"


        if ai_agent is not None:

            try:

                student_profile = {

                    "name":
                        data.get(
                            "name",
                            ""
                        ),

                    "email":
                        data.get(
                            "email",
                            ""
                        ),

                    "phone":
                        data.get(
                            "phone",
                            ""
                        ),

                    "location":
                        location,

                    "college":
                        data.get(
                            "college",
                            ""
                        ),

                    "degree":
                        data.get(
                            "degree",
                            ""
                        ),

                    "year":
                        data.get(
                            "year",
                            ""
                        ),

                    "skills":
                        skills,

                    "github":
                        data.get(
                            "github",
                            ""
                        ),

                    "linkedin":
                        data.get(
                            "linkedin",
                            ""
                        ),

                    "portfolio":
                        data.get(
                            "portfolio",
                            ""
                        ),

                    "projects":
                        data.get(
                            "projects",
                            ""
                        ),

                    "preferred_role":
                        role,

                    "work_preference":
                        data.get(
                            "work_preference",
                            data.get(
                                "location_preference",
                                ""
                            )
                        ),

                    "stipend_preference":
                        data.get(
                            "stipend_preference",
                            ""
                        ),

                    "duration_preference":
                        data.get(
                            "duration_preference",
                            ""
                        ),

                    "experience":
                        data.get(
                            "experience",
                            ""
                        ),

                    "learned_interests":
                        learned_interests

                }


                ai_answer = ai_agent.ask_ai(

                    keyword=keyword,

                    location=location,

                    internships=results,

                    student_profile=student_profile

                )


                ai_status = "success"


            except Exception as error:

                print(
                    "AI recommendation error:",
                    error
                )

                ai_status = "error"


        # -------------------------------------------------
        # RETURN RESULTS
        # -------------------------------------------------

        return jsonify({

            "success": True,

            "results": results,

            "count": len(results),

            "ai_answer": ai_answer,

            "ai_status": ai_status,

            "learned_interests":
                learned_interests

        })


    except Exception as error:

        print(
            "\nSEARCH ERROR:",
            error
        )

        return jsonify({

            "success": False,

            "message":
                "Unable to find internships.",

            "error":
                str(error)

        }), 500


# =========================================================
# PERSONALIZED RECOMMENDATIONS
# =========================================================

@app.route("/recommendations", methods=["GET"])
def recommendations():

    try:

        # -------------------------------------------------
        # GET USER
        # -------------------------------------------------

        user_id = request.args.get(
            "user_id",
            "guest"
        ).strip()


        # -------------------------------------------------
        # GET LEARNED INTERESTS
        # -------------------------------------------------

        learned_interests = get_user_interests(
            user_id,
            limit=20
        )


        print("\n======================================")
        print("PERSONALIZED RECOMMENDATIONS")
        print("User:", user_id)
        print("Interests:", learned_interests)
        print("======================================")


        # -------------------------------------------------
        # IF USER HAS NO HISTORY
        # -------------------------------------------------

        if not learned_interests:

            return jsonify({

                "success": True,

                "results": [],

                "count": 0,

                "learned_interests": [],

                "message":
                    "No learned interests yet. Search and interact with internships first."

            })


        # -------------------------------------------------
        # BUILD SEARCH KEYWORD
        # -------------------------------------------------

        # Use the strongest learned interests.

        top_interests = [
            item.get("interest", "")
            for item in learned_interests[:5]
            if item.get("interest")
        ]


        keyword = " ".join(
            top_interests
        ).strip()


        if not keyword:

            keyword = "internship"


        # -------------------------------------------------
        # SEARCH LIVE + DATASET INTERNSHIPS
        # -------------------------------------------------

        results = find_internships(

            keyword=keyword,

            location="India",

            user_skills=keyword,

            user_domain="",

            user_role=keyword,

            user_query=keyword,

            include_live=True,

            user_interests=learned_interests

        )


        # -------------------------------------------------
        # LIMIT RESULTS
        # -------------------------------------------------

        results = results[:20]


        # -------------------------------------------------
        # RETURN PERSONALIZED FEED
        # -------------------------------------------------

        return jsonify({

            "success": True,

            "results": results,

            "count": len(results),

            "learned_interests":
                learned_interests,

            "keyword":
                keyword

        })


    except Exception as error:

        print(
            "\nRECOMMENDATION ERROR:",
            error
        )

        return jsonify({

            "success": False,

            "message":
                "Unable to generate personalized recommendations.",

            "error":
                str(error)

        }), 500


# =========================================================
# TRACK USER BEHAVIOR
# =========================================================

@app.route("/track", methods=["POST"])
def track():

    try:

        data = request.get_json() or {}


        user_id = data.get(
            "user_id",
            "guest"
        )


        action = data.get(
            "action",
            "view"
        )


        record_interaction(

            user_id=user_id,

            action=action,

            internship_id=data.get(
                "internship_id",
                ""
            ),

            internship_title=data.get(
                "title",
                ""
            ),

            company=data.get(
                "company",
                ""
            ),

            skills=data.get(
                "skills",
                ""
            ),

            role=data.get(
                "role",
                ""
            ),

            location=data.get(
                "location",
                ""
            ),

            search_keyword=data.get(
                "search_keyword",
                ""
            )

        )


        updated_interests = get_user_interests(
            user_id
        )


        print(
            f"Tracked {action} for {user_id}"
        )


        return jsonify({

            "success": True,

            "learned_interests":
                updated_interests

        })


    except Exception as error:

        print(
            "Tracking error:",
            error
        )

        return jsonify({

            "success": False,

            "error":
                str(error)

        }), 500


# =========================================================
# USER INTERESTS
# =========================================================

@app.route("/interests", methods=["GET"])
def interests():

    user_id = request.args.get(
        "user_id",
        "guest"
    )


    user_interests = get_user_interests(
        user_id
    )


    return jsonify({

        "success": True,

        "user_id": user_id,

        "interests":
            user_interests

    })


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    print("\n======================================")
    print("      AI INTERNSHIP AGENT")
    print("======================================")
    print("Server running at:")
    print("http://127.0.0.1:5000")
    print("======================================\n")


    app.run(

        host="127.0.0.1",

        port=5000,

        debug=True

    )