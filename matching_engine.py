
import pandas as pd
import json

# STEP 1: Load datasets
students = pd.read_csv("data/students_with_clusters.csv")
companies = pd.read_csv("data/company_roles_cleaned.csv")

# STEP 2: Matching function
def calculate_match(student, required_skills):

    total_required = sum(required_skills.values())
    total_matched = 0
    missing_skills = []

    for skill, required_level in required_skills.items():

        student_level = student[skill]

        matched_level = min(student_level, required_level)

        total_matched += matched_level

        if student_level < required_level:
            missing_skills.append(skill)

    if total_required == 0:
        return 0, missing_skills

    percentage = (total_matched / total_required) * 100

    return round(percentage, 2), missing_skills


# STEP 3: Compare every student with every company role
all_results = []

for _, student in students.iterrows():

    for _, company in companies.iterrows():

        required_skills = json.loads(
            company["required_skills_json"]
        )

        match_percentage, missing_skills = calculate_match(
            student, required_skills
        )

        cgpa_eligible = (
            student["cgpa"] >= company["minimum_cgpa_template"]
        )

        all_results.append({

            "student_id": student["student_id"],
            "cluster": student["cluster"],
            "cgpa": student["cgpa"],
            "company": company["company"],
            "job_role": company["job_role"],
            "match_percentage": match_percentage,
            "cgpa_eligible": cgpa_eligible,
            "missing_skills": ", ".join(missing_skills)

        })


# STEP 4: Convert results into DataFrame
results_df = pd.DataFrame(all_results)

# STEP 5: Sort matching results
results_df = results_df.sort_values(
    by=["student_id", "match_percentage"],
    ascending=[True, False]
)

# STEP 6: Save all matching results
results_df.to_csv(
    "data/all_student_matching_results.csv",
    index=False
)

# STEP 7: Display final information
print("\n===== ALL STUDENT MATCHING RESULTS =====")

print("Total students:", len(students))
print("Total company roles:", len(companies))
print("Total comparisons:", len(results_df))

print("\nSample results:")
print(results_df.head(10).to_string(index=False))

print("\nAll student matching completed successfully!")
print("Results saved successfully!")
