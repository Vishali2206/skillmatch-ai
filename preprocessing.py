import pandas as pd
import numpy as np
# Load student dataset

df = pd.read_csv("data/students_synthetic.csv")

print(df.head())
print("Dataset Shape:", df.shape)

print("Column Names:")
print(df.columns)

print("Dataset Information:")
print(df.info())
# Check missing values

print("Missing Values:")

print(df.isnull().sum())
# Check duplicate records

print("Duplicate Records:")

print(df.duplicated().sum())
print("Duplicate Student IDs:")

print(df["student_id"].duplicated().sum())
# Remove completely duplicated records

df = df.drop_duplicates()

# Remove records with duplicate student IDs,
# keeping the first occurrence

df = df.drop_duplicates(
    subset=["student_id"],
    keep="first"
)

# Identify numerical columns

numeric_cols = df.select_dtypes(
    include=np.number
).columns

# Fill missing numerical values with column median

df[numeric_cols] = df[numeric_cols].fillna(
    df[numeric_cols].median()
)

print("Data Cleaning Completed!")
# Select features for Machine Learning

features = [
    "cgpa",
    "python",
    "java",
    "cpp",
    "html_css",
    "javascript",
    "react",
    "sql",
    "data_analytics",
    "machine_learning",
    "dsa",
    "communication",
    "problem_solving"
]

X = df[features]

print("Selected Features:")
print(X.head())
from sklearn.preprocessing import StandardScaler

# Create scaler

scaler = StandardScaler()

# Transform student features

X_scaled = scaler.fit_transform(X)

print("Scaled Data:")
print(X_scaled[:5])
# Save cleaned dataset

df.to_csv(
    "data/students_cleaned.csv",
    index=False
)

# Save scaled dataset

scaled_df = pd.DataFrame(
    X_scaled,
    columns=features
)

scaled_df.insert(
    0,
    "student_id",
    df["student_id"].values
)

scaled_df.to_csv(
    "data/students_scaled.csv",
    index=False
)

print("Datasets saved successfully!")