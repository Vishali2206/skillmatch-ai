
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# PAGE CONFIGURATION
st.set_page_config(
    page_title="SkillMatch AI",
    page_icon="🎯",
    layout="wide"
)

# LOAD DATA
@st.cache_data
def load_data():

    students = pd.read_csv(
        "data/students_with_clusters.csv"
    )

    profiles = pd.read_csv(
        "data/cluster_analysis.csv"
    )

    companies = pd.read_csv(
        "data/company_roles_cleaned.csv"
    )

    matches = pd.read_csv(
        "data/all_student_matching_results.csv"
    )

    recommendations = pd.read_csv(
        "data/skill_recommendations.csv"
    )

    return students, profiles, companies, matches, recommendations


students, profiles, companies, matches, recommendations = load_data()

# HEADER
st.title("🎯 SkillMatch AI")
st.subheader("Student Skill Analysis & Company Recommendation System")

st.write(
    "An AI-powered student clustering and company-role "
    "matching platform using Machine Learning."
)

st.divider()

# SIDEBAR
st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Choose a section",
    [
        "Dashboard Overview",
        "Student Analysis",
        "Company Matching",
        "Skill Gap Recommendations"
    ]
)

# PAGE 1: OVERVIEW
if page == "Dashboard Overview":

    st.header("Project Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Students", len(students))
    col2.metric("Student Clusters", students["cluster"].nunique())
    col3.metric("Company Roles", len(companies))
    col4.metric("Total Comparisons", len(matches))

    st.divider()

    st.subheader("Student Distribution Across Clusters")

    cluster_counts = (
        students["cluster"]
        .value_counts()
        .sort_index()
    )

    fig, ax = plt.subplots(figsize=(9, 4))

    cluster_counts.plot(
        kind="bar",
        ax=ax
    )

    ax.set_xlabel("Cluster")
    ax.set_ylabel("Number of Students")
    ax.set_title("K-Means Cluster Distribution")

    st.pyplot(fig)
    plt.close(fig)

    st.subheader("Average Skill Category Scores")

    categories = [
        "Web Development",
        "Data Analytics",
        "Java/Software",
        "Machine Learning"
    ]

    st.dataframe(
        profiles[
            ["cluster"] + categories
        ].round(2),
        use_container_width=True,
        hide_index=True
    )

# PAGE 2: STUDENT ANALYSIS
elif page == "Student Analysis":

    st.header("Individual Student Analysis")

    selected_student = st.selectbox(
        "Select Student ID",
        students["student_id"].tolist()
    )

    student = students[
        students["student_id"] == selected_student
    ].iloc[0]

    col1, col2, col3 = st.columns(3)

    col1.metric("Student ID", student["student_id"])
    col2.metric("CGPA", round(student["cgpa"], 2))
    col3.metric("Cluster", int(student["cluster"]))

    st.subheader("Technical Skill Profile")

    skill_columns = [
        "python", "java", "cpp",
        "html_css", "javascript", "react",
        "sql", "data_analytics",
        "machine_learning", "dsa",
        "communication", "problem_solving"
    ]

    skill_values = [
        student[skill] for skill in skill_columns
    ]

    fig, ax = plt.subplots(figsize=(11, 5))

    ax.bar(skill_columns, skill_values)

    ax.set_ylabel("Skill Level (0–5)")
    ax.set_ylim(0, 5)
    ax.set_xticklabels(
        skill_columns,
        rotation=45,
        ha="right"
    )

    ax.set_title("Student Skill Distribution")

    st.pyplot(fig)
    plt.close(fig)

# PAGE 3: COMPANY MATCHING
elif page == "Company Matching":

    st.header("Company Role Matching")

    selected_student = st.selectbox(
        "Select Student",
        students["student_id"].tolist(),
        key="matching_student"
    )

    student_matches = matches[
        matches["student_id"] == selected_student
    ].sort_values(
        "match_percentage",
        ascending=False
    )

    st.subheader("Top Company Recommendations")

    st.dataframe(
        student_matches[
            [
                "company",
                "job_role",
                "match_percentage",
                "cgpa_eligible",
                "missing_skills"
            ]
        ].head(10),
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        "CGPA eligibility uses illustrative template thresholds, "
        "not verified current recruitment criteria."
    )

# PAGE 4: SKILL GAP
elif page == "Skill Gap Recommendations":

    st.header("Skill Gap Analysis")

    selected_student = st.selectbox(
        "Select Student",
        students["student_id"].tolist(),
        key="recommendation_student"
    )

    student_recommendations = recommendations[
        recommendations["student_id"] == selected_student
    ]

    if student_recommendations.empty:

        st.success(
            "No missing skills identified for the selected recommended role."
        )

    else:

        st.subheader("Recommended Improvements")

        st.dataframe(
            student_recommendations[
                [
                    "recommended_company",
                    "recommended_role",
                    "match_percentage",
                    "missing_skill",
                    "improvement_action"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

st.divider()

st.caption(
    "SkillMatch AI | B.Tech Machine Learning Project | "
    "Educational prototype using synthetic student data."
)
