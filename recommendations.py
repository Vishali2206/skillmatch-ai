
import pandas as pd

# STEP 1: Load datasets
students = pd.read_csv("data/students_with_clusters.csv")

matches = pd.read_csv(
    "data/all_student_matching_results.csv"
)

# STEP 2: Define improvement recommendations
skill_recommendations = {

    "python": "Practice Python programming and build projects.",
    "java": "Learn Java fundamentals and OOP concepts.",
    "cpp": "Practice C++ programming and problem solving.",
    "html_css": "Build responsive websites using HTML and CSS.",
    "javascript": "Learn JavaScript and DOM manipulation.",
    "react": "Build interactive projects using React.",
    "sql": "Practice SQL queries and database management.",
    "data_analytics": "Learn Excel, Pandas and data visualization.",
    "machine_learning": "Study ML algorithms and build ML projects.",
    "dsa": "Practice Data Structures and Algorithms.",
    "communication": "Improve communication and presentation skills.",
    "problem_solving": "Solve coding problems regularly."
}

# STEP 3: Generate recommendations
all_recommendations = []

for _, student in students.iterrows():

    student_matches = matches[
        matches["student_id"] == student["student_id"]
    ]

    # Select highest skill match among CGPA-eligible roles.
    eligible_matches = student_matches[
        student_matches["cgpa_eligible"] == True
    ]

    if eligible_matches.empty:
        best_match = student_matches.sort_values(
            "match_percentage", ascending=False
        ).iloc[0]

        eligibility_note = "No sample CGPA-eligible role"
    else:
        best_match = eligible_matches.sort_values(
            "match_percentage", ascending=False
        ).iloc[0]

        eligibility_note = "Meets sample CGPA threshold"

    missing_skills = best_match["missing_skills"]

    if pd.isna(missing_skills) or not str(missing_skills).strip():
        missing_skills_list = []
    else:
        missing_skills_list = [
            skill.strip()
            for skill in str(missing_skills).split(",")
        ]

    for skill in missing_skills_list:

        all_recommendations.append({

            "student_id": student["student_id"],
            "cluster": student["cluster"],
            "recommended_company": best_match["company"],
            "recommended_role": best_match["job_role"],
            "match_percentage": best_match["match_percentage"],
            "eligibility_note": eligibility_note,
            "missing_skill": skill,
            "improvement_action": skill_recommendations.get(
                skill, "Improve this skill through practice."
            )

        })

# STEP 4: Save recommendations
recommendations_df = pd.DataFrame(all_recommendations)

recommendations_df.to_csv(
    "data/skill_recommendations.csv",
    index=False
)

# STEP 5: Display results
print("\n===== SKILL GAP ANALYSIS =====")

print("Total recommendations:", len(recommendations_df))

print("\nSample recommendations:")

if not recommendations_df.empty:
    print(recommendations_df.head(15).to_string(index=False))
else:
    print("No skill gaps found for selected matches.")

print("\nSkill gap analysis completed!")
print("Recommendations saved successfully!")
