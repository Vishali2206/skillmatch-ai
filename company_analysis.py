
import pandas as pd
import json

# STEP 1: Load company dataset
df = pd.read_csv("data/company_roles_template.csv")

print("===== COMPANY DATASET ANALYSIS =====")

# STEP 2: Display dataset information
print("\nTotal company-role records:", len(df))
print("\nCompany names:")
print(df["company"].to_list())

# STEP 3: Check missing values
print("\nMissing values:")
print(df.isnull().sum())

# STEP 4: Validate required skills JSON
valid_records = 0
invalid_records = 0

for index, row in df.iterrows():

    try:
        skills = json.loads(row["required_skills_json"])

        # Check that skill levels are between 0 and 5
        if all(
            isinstance(value, (int, float))
            and 0 <= value <= 5
            for value in skills.values()
        ):
            valid_records += 1
        else:
            invalid_records += 1

    except (json.JSONDecodeError, TypeError):
        invalid_records += 1

# STEP 5: Display validation results
print("\nValid skill records:", valid_records)
print("Invalid skill records:", invalid_records)

# STEP 6: Save company dataset copy
df.to_csv("data/company_roles_cleaned.csv", index=False)

print("\nCompany dataset validation completed!")
print("Cleaned dataset saved successfully!")
