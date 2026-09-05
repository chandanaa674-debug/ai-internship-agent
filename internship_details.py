
"""
internship_details.py

Processes and standardizes internship information.

Required output fields:
- title
- company
- location
- skills
- eligibility
- duration
- stipend
- description
- apply_url
"""


def get_value(data, *keys, default="Not Available"):
    """
    Return the first useful value found for the given keys.
    """

    for key in keys:
        value = data.get(key)

        if value is None:
            continue

        if isinstance(value, str):
            value = value.strip()

            if value:
                return value

        elif isinstance(value, list):
            values = [
                str(item).strip()
                for item in value
                if str(item).strip()
            ]

            if values:
                return ", ".join(values)

        else:
            return str(value)

    return default


def process_details(internship):
    """
    Convert one raw internship record into a standard format.
    """

    if not isinstance(internship, dict):
        return None

    title = get_value(
        internship,
        "title",
        "job_title",
        "name",
        default="Internship Opportunity"
    )

    company = get_value(
        internship,
        "company",
        "company_name",
        "organization",
        "employer",
        default="Company Not Available"
    )

    location = get_value(
        internship,
        "location",
        "locations",
        "city",
        "place",
        default="Location Not Available"
    )

    skills = get_value(
        internship,
        "skills",
        "skill",
        "technologies",
        "technology",
        "tags",
        default="Not Available"
    )

    eligibility = get_value(
        internship,
        "eligibility",
        "requirements",
        "qualification",
        "qualifications",
        default="Not Available"
    )

    duration = get_value(
        internship,
        "duration",
        "internship_duration",
        default="Not Available"
    )

    stipend = get_value(
        internship,
        "stipend",
        "salary",
        "pay",
        "compensation",
        default="Not Available"
    )

    description = get_value(
        internship,
        "description",
        "job_description",
        "summary",
        "details",
        default="No description available."
    )

    apply_url = get_value(
        internship,
        "apply_url",
        "url",
        "apply",
        "apply_link",
        "link",
        default=""
    )

    return {
        "title": title,
        "company": company,
        "location": location,
        "skills": skills,
        "eligibility": eligibility,
        "duration": duration,
        "stipend": stipend,
        "description": description,
        "apply_url": apply_url
    }


def process_all_details(internships):
    """
    Process every internship returned by the search module.
    """

    if not isinstance(internships, list):
        return []

    processed_internships = []

    for internship in internships:

        processed = process_details(internship)

        if processed is not None:
            processed_internships.append(processed)

    return processed_internships


if __name__ == "__main__":

    print("=" * 70)
    print("INTERNSHIP DETAILS MODULE TEST")
    print("=" * 70)

    sample_internships = [
        {
            "title": "Python Developer Intern",
            "company": "Example Technologies",
            "location": "Bengaluru, India",
            "skills": ["Python", "Flask", "SQL"],
            "eligibility": "Computer Science students",
            "duration": "3 Months",
            "stipend": "₹15,000/month",
            "description": "Work on Python backend applications.",
            "apply_url": "https://example.com/python-intern"
        },

        {
            "title": "AI/ML Intern",
            "company": "AI Solutions",
            "location": "Hyderabad, India",
            "skills": ["Python", "Machine Learning"],
            "eligibility": "Students with ML knowledge",
            "duration": "6 Months",
            "stipend": "₹20,000/month",
            "description": "Assist with machine learning projects.",
            "apply_url": "https://example.com/aiml-intern"
        },

        {
            "title": "Data Science Intern",
            "company": "Data Labs",
            "location": "Pune, India",
            "skills": ["Python", "Pandas", "SQL"],
            "eligibility": "Data Science students",
            "duration": "3 Months",
            "stipend": "₹12,000/month",
            "description": "Analyze datasets and create reports.",
            "apply_url": "https://example.com/data-intern"
        },

        {
            "title": "Web Development Intern",
            "company": "WebWorks",
            "location": "Remote",
            "skills": ["HTML", "CSS", "JavaScript"],
            "eligibility": "Web development students",
            "duration": "4 Months",
            "stipend": "₹10,000/month",
            "description": "Build and maintain web applications.",
            "apply_url": "https://example.com/web-intern"
        },

        {
            "title": "Software Engineering Intern",
            "company": "Tech Systems",
            "location": "Chennai, India",
            "skills": ["Python", "Git", "APIs"],
            "eligibility": "Engineering students",
            "duration": "6 Months",
            "stipend": "₹18,000/month",
            "description": "Help develop and test software systems.",
            "apply_url": "https://example.com/software-intern"
        }
    ]

    results = process_all_details(
        sample_internships
    )

    print()
    print(f"Processed internships: {len(results)}")
    print()

    for index, internship in enumerate(results, 1):

        print("-" * 70)
        print(f"INTERNSHIP {index}")
        print("-" * 70)

        print(f"Title       : {internship['title']}")
        print(f"Company     : {internship['company']}")
        print(f"Location    : {internship['location']}")
        print(f"Skills      : {internship['skills']}")
        print(f"Eligibility : {internship['eligibility']}")
        print(f"Duration    : {internship['duration']}")
        print(f"Stipend     : {internship['stipend']}")
        print(f"Description : {internship['description']}")
        print(f"Apply URL   : {internship['apply_url']}")

    print()
    print("=" * 70)
    print("TEST COMPLETED SUCCESSFULLY")
    print("=" * 70)

