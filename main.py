from flask import Flask, render_template, request, jsonify
from agent.agent import InternshipAgent

app = Flask(__name__)

agent = InternshipAgent()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/search", methods=["POST"])
def search():
    try:
        data = request.get_json(silent=True)

        if not data:
            return jsonify({
                "success": False,
                "message": "No search data received."
            }), 400

        keyword = str(data.get("keyword", "")).strip()
        location = str(data.get("location", "India")).strip()

        if not keyword:
            return jsonify({
                "success": False,
                "message": "Please enter an internship skill."
            }), 400

        if not location:
            location = "India"

        print()
        print("=" * 70)
        print("INTERNSHIP SEARCH")
        print("=" * 70)
        print("Skill:", keyword)
        print("Location:", location)
        print("=" * 70)

        result = agent.ask_ai(
            keyword=keyword,
            location=location,
            limit=20
        )

        results = result.get("results", [])

        print("Opportunities found:", len(results))
        print("=" * 70)

        return jsonify({
            "success": True,
            "message": "Internship search completed.",
            "results": results,
            "answer": result.get("answer", ""),
            "ai_used": result.get("ai_used", False),
            "model": result.get("model")
        })

    except Exception as error:
        print()
        print("=" * 70)
        print("FLASK SEARCH ERROR")
        print("=" * 70)
        print(str(error))
        print("=" * 70)

        return jsonify({
            "success": False,
            "message": "Unable to search internships.",
            "error": str(error)
        }), 500


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )