# 🤖 AI Internship Agent

An AI-powered internship discovery and recommendation system that helps students search for internship opportunities based on their **skills and preferred location**.

The system combines internship searching, information processing, ranking, and an AI assistant to provide relevant internship recommendations through a simple web interface.

---

## 📌 Project Overview

Finding suitable internships can be time-consuming because students need to search through different job listings and compare opportunities manually.

The **AI Internship Agent** is designed to simplify this process.

A user provides:

* 💻 Internship skill
* 📍 Preferred location

The system searches available internship listings, processes the information, ranks the opportunities, and presents the results through a web interface.

---

## ✨ Features

* 🔎 Internship search based on skills
* 📍 Location-based internship filtering
* 📊 Internship information processing
* ⭐ Internship ranking and matching
* 🤖 AI-assisted internship recommendations
* 🌐 Web-based user interface
* 🔗 Application links for internship opportunities
* 🧩 Modular agent architecture
* 🔐 Environment variable support for API credentials

---

## 🏗️ System Architecture

```text
                 ┌──────────────────────┐
                 │        User          │
                 │ Skill + Location     │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │    Flask Frontend    │
                 │    HTML + CSS        │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │ Internship Search    │
                 │ internship_search.py  │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │ Internship Processor │
                 │ internship_processor │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │ Internship Ranker    │
                 │ internship_ranker.py │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │     AI Agent         │
                 │    agent/agent.py    │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │ Internship Results    │
                 │ + AI Recommendations  │
                 └──────────────────────┘
```

---

## 📂 Project Structure

```text
internship-agent/
│
├── internship_details.py
├── internship_processor.py
├── internship_ranker.py
├── internship_search.py
├── main.py
├── requirements.txt
├── .env
├── .gitignore
├── README.md
│
├── agent/
│   ├── __init__.py
│   ├── agent.py
│   └── prompts.py
│
├── static/
│   └── style.css
│
└── templates/
    └── index.html
```

### File Description

| File                      | Purpose                                                  |
| ------------------------- | -------------------------------------------------------- |
| `main.py`                 | Runs the Flask web application                           |
| `internship_search.py`    | Searches internship opportunities                        |
| `internship_details.py`   | Processes and standardizes internship information        |
| `internship_processor.py` | Connects searching, processing, and ranking              |
| `internship_ranker.py`    | Calculates internship matching scores                    |
| `agent/agent.py`          | Handles the AI internship assistant                      |
| `agent/prompts.py`        | Contains AI prompts                                      |
| `templates/index.html`    | Frontend webpage                                         |
| `static/style.css`        | Frontend styling                                         |
| `requirements.txt`        | Python dependencies                                      |
| `.env`                    | Stores private API credentials                           |
| `.gitignore`              | Prevents sensitive/unnecessary files from being uploaded |
| `README.md`               | Project documentation                                    |

---

## 🛠️ Technologies Used

* **Python**
* **Flask**
* **HTML**
* **CSS**
* **REST API**
* **Google Gemini**
* **Requests**
* **python-dotenv**

---

## ⚙️ How It Works

### Step 1 — User Input

The user enters:

```text
Skill: Python
Location: Bangalore
```

### Step 2 — Internship Search

The system searches available internship listings using the requested skill and location.

### Step 3 — Data Processing

The internship information is standardized into fields such as:

* Title
* Company
* Location
* Skills
* Eligibility
* Duration
* Stipend
* Description
* Application URL

### Step 4 — Ranking

The internship ranker calculates a matching score based on factors such as:

* Skill match
* Location match
* Job title
* Eligibility
* Stipend
* Duration

### Step 5 — AI Assistant

The processed internship information is passed to the AI agent.

The AI assistant can help summarize and explain the available opportunities.

### Step 6 — Results

The user receives internship opportunities through the web interface.

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Open the project

```bash
cd internship-agent
```

### 3. Create a virtual environment

Windows:

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root.

```text
GEMINI_API_KEY=your_api_key_here
```

**Never upload your real API key to GitHub.**

The `.env` file should remain ignored through `.gitignore`.

Example `.gitignore`:

```text
.env
__pycache__/
*.pyc
venv/
.venv/
```

---

## ▶️ Running the Project

From the project directory:

```bash
python main.py
```

The Flask application will start locally.

Open the local address displayed in the terminal in your browser.

---

## 🧪 Testing the AI Agent

The AI agent can also be tested directly using:

```bash
python -m agent.agent
```

The program asks for:

```text
Enter internship skill:
Enter location:
```

For example:

```text
Enter internship skill: Python
Enter location: Bangalore
```

---

## 📋 Example Workflow

```text
User enters:

Skill → Python
Location → Bangalore

        ↓

Internship Search

        ↓

Internship Processing

        ↓

Internship Ranking

        ↓

AI Agent

        ↓

Recommended Internship Opportunities
```

---

## 🎯 Project Objective

The main objective of this project is to build an AI-based assistant that reduces the time students spend searching for suitable internship opportunities.

The project demonstrates the integration of:

* Python programming
* Web development
* REST APIs
* Data processing
* Ranking algorithms
* Generative AI
* Flask
* Modular software architecture

---

## 🔮 Future Improvements

The project can be extended with:

* More internship data sources
* More reliable India-specific internship sources
* Advanced semantic skill matching
* Resume-based internship recommendations
* User profiles
* Internship bookmarking
* Email notifications
* Automatic application tracking
* Personalized recommendations
* Improved location filtering
* Deployment to a cloud platform

---

## ⚠️ Limitations

The availability and accuracy of internship results depend on the external job data source.

Therefore, the system should be considered an **internship discovery and recommendation prototype**, rather than a guarantee that every displayed opportunity is currently available.

Users should verify the internship details and application status on the original job listing before applying.

---

## 👩‍💻 Author

**Chandana A**

AI Internship Agent Project

---

## 📄 License

This project is created for educational and internship/project demonstration purposes.
