
import pandas as pd

# STEP 1: Load cluster profiles
df = pd.read_csv("data/cluster_profiles.csv", index_col=0)

# STEP 2: Calculate average scores for each career category
df["Web Development"] = df[
    ["html_css", "javascript", "react"]
].mean(axis=1)

df["Data Analytics"] = df[
    ["python", "sql", "data_analytics"]
].mean(axis=1)

df["Java/Software"] = df[
    ["java", "cpp", "dsa"]
].mean(axis=1)

df["Machine Learning"] = df[
    ["python", "machine_learning", "data_analytics"]
].mean(axis=1)

# STEP 3: Find the strongest category in each cluster
categories = [
    "Web Development",
    "Data Analytics",
    "Java/Software",
    "Machine Learning"
]

df["Suggested Cluster Name"] = (
    df[categories].idxmax(axis=1)
)

# STEP 4: Display results
print("\n===== STUDENT CLUSTER ANALYSIS =====")

print(
    df[
        categories + ["Suggested Cluster Name"]
    ].round(2).to_string()
)

# STEP 5: Save analysis
df.to_csv("data/cluster_analysis.csv")

print("\nAnalysis saved successfully!")
