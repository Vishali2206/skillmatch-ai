
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

# STEP 1: Load scaled dataset
df = pd.read_csv("data/students_scaled.csv")

# STEP 2: Select features
features = [
    "cgpa", "python", "java", "cpp",
    "html_css", "javascript", "react",
    "sql", "data_analytics",
    "machine_learning", "dsa",
    "communication", "problem_solving"
]

X = df[features]

print("Dataset loaded:", X.shape)

# STEP 3: Elbow Method
wcss = []

for i in range(1, 11):

    model = KMeans(
        n_clusters=i,
        random_state=42,
        n_init=10
    )

    model.fit(X)

    wcss.append(model.inertia_)

plt.figure(figsize=(8, 5))
plt.plot(range(1, 11), wcss, marker="o")

plt.title("Elbow Method")
plt.xlabel("Number of Clusters (K)")
plt.ylabel("WCSS / Inertia")
plt.xticks(range(1, 11))
plt.grid(True)

plt.savefig("data/elbow_method.png")
plt.show()

# STEP 4: Apply K-Means
kmeans = KMeans(
    n_clusters=4,
    random_state=42,
    n_init=10
)

df["cluster"] = kmeans.fit_predict(X)

print("\nClustering completed!")

# STEP 5: Count students
print("\nCluster Distribution:")
print(df["cluster"].value_counts().sort_index())

# STEP 6: Load original cleaned data
original_df = pd.read_csv("data/students_cleaned.csv")

original_df["cluster"] = df["cluster"].values

# STEP 7: Calculate cluster profiles
cluster_profiles = original_df.groupby(
    "cluster"
)[features].mean()

print("\nCluster Skill Profiles:")
print(cluster_profiles.round(2))

# STEP 8: Cluster distribution graph
plt.figure(figsize=(8, 5))

df["cluster"].value_counts().sort_index().plot(
    kind="bar",
    color="steelblue"
)

plt.title("Student Distribution Across Clusters")
plt.xlabel("Cluster")
plt.ylabel("Number of Students")

plt.tight_layout()
plt.savefig("data/cluster_distribution.png")
plt.show()

# STEP 9: PCA visualization
pca = PCA(n_components=2)

X_pca = pca.fit_transform(X)

plt.figure(figsize=(8, 6))

plt.scatter(
    X_pca[:, 0],
    X_pca[:, 1],
    c=df["cluster"],
    cmap="viridis",
    s=40
)

plt.title("Student Clusters using K-Means")
plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")
plt.colorbar(label="Cluster")

plt.tight_layout()
plt.savefig("data/student_clusters_pca.png")
plt.show()

# STEP 10: Save results
original_df.to_csv(
    "data/students_with_clusters.csv",
    index=False
)

cluster_profiles.to_csv(
    "data/cluster_profiles.csv"
)

print("\nAll results saved successfully!")
print("Total students:", len(original_df))
print("Total clusters:", original_df["cluster"].nunique())

