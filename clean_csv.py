
import pandas as pd
import ast

# ============================================================
# FILE SETTINGS
# ============================================================

# Your original Kaggle CSV
input_file = "data/cleaned_data.csv"

# Clean CSV that will be used by our internship agent
output_file = "data/internship_agent_dataset.csv"


# ============================================================
# READ DATA
# ============================================================

try:
    df = pd.read_csv(input_file)
except FileNotFoundError:
    print(f"ERROR: {input_file} was not found.")
    print("Make sure dataset.csv is inside the same folder as this Python file.")
    exit()

print("Original dataset loaded successfully!")
print("Original rows:", len(df))
print("Original columns:")
print(df.columns.tolist())


# ============================================================
# CHECK REQUIRED COLUMNS
# ============================================================

required_columns = [
    "title",
    "processed_desc",
    "job_skills",
    "job_domain",
    "type"
]

missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

if missing_columns:
    print("\nERROR: These columns are missing:")
    print(missing_columns)
    print("\nAvailable columns are:")
    print(df.columns.tolist())
    exit()


# ============================================================
# FUNCTION 1: CONVERT LIST DATA INTO TEXT
# ============================================================

def parse_list(value):

    if pd.isna(value):
        return []

    text = str(value).strip()

    if not text:
        return []

    try:
        data = ast.literal_eval(text)

        if isinstance(data, list):
            return [
                str(item).strip()
                for item in data
                if str(item).strip()
            ]

        return [str(data).strip()]

    except Exception:

        # If the value is not a Python list,
        # treat it as comma-separated text.

        text = text.strip("[]")

        return [
            item.strip().strip("'").strip('"')
            for item in text.split(",")
            if item.strip()
        ]


# ============================================================
# FUNCTION 2: EXTRACT JOB DESCRIPTION
# ============================================================

def extract_description(value):

    if pd.isna(value):
        return ""

    text = str(value).strip()

    if not text:
        return ""

    try:

        data = ast.literal_eval(text)

        # Some Kaggle records contain a dictionary
        # with "lemmatized" and "original" fields.

        if isinstance(data, dict):

            # Prefer cleaned description
            if data.get("lemmatized"):

                lemmatized = data["lemmatized"]

                if isinstance(lemmatized, list):
                    return " ".join(
                        str(item) for item in lemmatized
                    )

                return str(lemmatized)

            # Otherwise use original description
            if data.get("original"):

                original = data["original"]

                if isinstance(original, list):
                    return " ".join(
                        str(item) for item in original
                    )

                return str(original)

    except Exception:
        pass

    return text


# ============================================================
# CREATE CLEAN DATASET
# ============================================================

result = pd.DataFrame()


# ------------------------------------------------------------
# Internship ID
# ------------------------------------------------------------

result["internship_id"] = range(1, len(df) + 1)


# ------------------------------------------------------------
# Title
# ------------------------------------------------------------

result["title"] = (
    df["title"]
    .fillna("")
    .astype(str)
    .str.strip()
)


# ------------------------------------------------------------
# Company
# ------------------------------------------------------------

# The supplied Kaggle dataset does not reliably provide
# company information, so we do NOT invent it.

result["company"] = ""


# ------------------------------------------------------------
# Location
# ------------------------------------------------------------

# The supplied Kaggle dataset does not reliably provide
# location information, so we leave it blank.

result["location"] = ""


# ------------------------------------------------------------
# Description
# ------------------------------------------------------------

result["description"] = (
    df["processed_desc"]
    .apply(extract_description)
    .astype(str)
    .str.replace(r"\s+", " ", regex=True)
    .str.strip()
)


# ------------------------------------------------------------
# Skills
# ------------------------------------------------------------

result["skills"] = (
    df["job_skills"]
    .apply(parse_list)
    .apply(lambda skills: ", ".join(skills))
)


# ------------------------------------------------------------
# Domain
# ------------------------------------------------------------

result["domain"] = (
    df["job_domain"]
    .apply(parse_list)
    .apply(lambda domains: ", ".join(domains))
)


# ------------------------------------------------------------
# Job Type
# ------------------------------------------------------------

result["job_type"] = (
    df["type"]
    .fillna("")
    .astype(str)
    .str.strip()
)


# ------------------------------------------------------------
# Source
# ------------------------------------------------------------

result["source"] = "Kaggle"


# ============================================================
# REMOVE INVALID RECORDS
# ============================================================

# Remove records without title
result = result[
    result["title"].str.strip() != ""
]

# Remove records without description
result = result[
    result["description"].str.strip() != ""
]


# ============================================================
# REMOVE DUPLICATES
# ============================================================

result = result.drop_duplicates(
    subset=["title", "description"]
).reset_index(drop=True)


# ============================================================
# RE-CREATE INTERNSHIP IDs
# ============================================================

result["internship_id"] = range(
    1,
    len(result) + 1
)


# ============================================================
# FINAL COLUMN ORDER
# ============================================================

result = result[
    [
        "internship_id",
        "title",
        "company",
        "location",
        "description",
        "skills",
        "domain",
        "job_type",
        "source"
    ]
]


# ============================================================
# SAVE CLEAN DATASET
# ============================================================

result.to_csv(
    output_file,
    index=False,
    encoding="utf-8"
)


# ============================================================
# DISPLAY RESULTS
# ============================================================

print("\n==========================================")
print("DATASET CLEANED SUCCESSFULLY")
print("==========================================")

print("\nOutput file:")
print(output_file)

print("\nNumber of cleaned records:")
print(len(result))

print("\nFinal columns:")
print(result.columns.tolist())

print("\nFirst 5 records:")
print(result.head(5).to_string(index=False))

print("\n==========================================")
print("NEXT STEP")
print("==========================================")

print(
    "\nUse internship_agent_dataset.csv "
    "as the dataset for your recommendation system."
)

