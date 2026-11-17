
from pathlib import Path

import pandas as pd
import streamlit as st
import plotly.express as px


# ============================================================
# 1. PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="SkillMatch AI | Student Intelligence",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# 2. FOREST & IVORY DESIGN SYSTEM
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');

:root {
    --ivory: #F7F7F2;
    --white: #FFFFFF;
    --forest: #246B50;
    --forest-dark: #194D3A;
    --sage: #A9B9A5;
    --charcoal: #202522;
    --muted: #707A72;
    --border: #E5E9E2;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background: #F7F7F2;
    color: #202522;
}

.block-container {
    max-width: 1500px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* SIDEBAR */

section[data-testid="stSidebar"] {
    background: #202C25;
    border-right: 1px solid #344239;
}

section[data-testid="stSidebar"] * {
    color: #F4F5EF;
}

section[data-testid="stSidebar"] label {
    color: #F4F5EF !important;
}

section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    color: #D0DAD1;
}

/* HEADINGS */

h1, h2, h3 {
    font-family: 'Manrope', sans-serif !important;
    color: #202522 !important;
    letter-spacing: -0.5px;
}

h1 {
    font-weight: 800 !important;
}

h2, h3 {
    font-weight: 700 !important;
}

/* METRIC CARDS */

div[data-testid="stMetric"] {
    background: #FFFFFF;
    border: 1px solid #E5E9E2;
    border-radius: 13px;
    padding: 18px 20px;
    box-shadow: 0 2px 8px rgba(32,37,34,0.025);
}

div[data-testid="stMetricLabel"] {
    color: #707A72;
    font-size: 13px;
    font-weight: 600;
}

div[data-testid="stMetricValue"] {
    color: #246B50;
    font-family: 'Manrope', sans-serif;
    font-weight: 800;
}

/* BUTTONS */

.stButton > button {
    background: #246B50;
    color: #FFFFFF;
    border: 1px solid #246B50;
    border-radius: 8px;
    font-weight: 600;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    background: #194D3A;
    color: #FFFFFF;
    border-color: #194D3A;
}

/* INPUTS */

div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div {
    border-radius: 8px;
    border-color: #E5E9E2;
}

/* DATA TABLES */

div[data-testid="stDataFrame"] {
    border: 1px solid #E5E9E2;
    border-radius: 10px;
    overflow: hidden;
}

/* EXPANDERS */

div[data-testid="stExpander"] {
    background: #FFFFFF;
    border: 1px solid #E5E9E2;
    border-radius: 10px;
}

/* TABS */

button[data-baseweb="tab"] {
    font-weight: 600;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #246B50 !important;
}

/* DIVIDERS */

hr {
    border-color: #E5E9E2;
}

/* CAPTIONS */

.stCaption {
    color: #707A72;
}

/* HIDE STREAMLIT BRANDING */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# 3. LOAD PROJECT DATA
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

FILE_PATHS = {
    "students": DATA_DIR / "students_with_clusters.csv",
    "profiles": DATA_DIR / "cluster_analysis.csv",
    "companies": DATA_DIR / "company_roles_cleaned.csv",
    "matches": DATA_DIR / "all_student_matching_results.csv",
    "recommendations": DATA_DIR / "skill_recommendations.csv"
}


@st.cache_data
def load_data():

    loaded = {}

    for name, path in FILE_PATHS.items():

        if not path.exists():
            raise FileNotFoundError(
                f"File not found: {path}"
            )

        loaded[name] = pd.read_csv(path)

    return loaded


try:

    data = load_data()

    students = data["students"].copy()
    profiles = data["profiles"].copy()
    companies = data["companies"].copy()
    matches = data["matches"].copy()
    recommendations = data["recommendations"].copy()

except Exception as error:

    st.error("Unable to load project data.")
    st.exception(error)

    st.info(
        "Please check that all five CSV files are inside your data folder."
    )

    st.stop()


# ============================================================
# 4. DATA VALIDATION
# ============================================================

required_columns = {
    "students": ["student_id", "cluster", "cgpa"],
    "matches": [
        "student_id",
        "company",
        "job_role",
        "match_percentage"
    ],
    "profiles": ["cluster"]
}

datasets = {
    "students": students,
    "matches": matches,
    "profiles": profiles
}

for dataset_name, required in required_columns.items():

    missing = [
        column for column in required
        if column not in datasets[dataset_name].columns
    ]

    if missing:

        st.error(
            f"{dataset_name} is missing columns: {missing}"
        )

        st.stop()


# ============================================================
# 5. SKILL CONFIGURATION
# ============================================================

skill_columns = [
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

available_skills = [
    skill for skill in skill_columns
    if skill in students.columns
]

category_columns = [
    "Web Development",
    "Data Analytics",
    "Java/Software",
    "Machine Learning"
]

available_categories = [
    category for category in category_columns
    if category in profiles.columns
]


# ============================================================
# 6. HELPER FUNCTIONS
# ============================================================

def get_student(student_id):

    result = students[
        students["student_id"].astype(str)
        == str(student_id)
    ]

    if result.empty:
        return None

    return result.iloc[0]


def get_cluster_name(cluster_id):

    result = profiles[
        profiles["cluster"].astype(str)
        == str(cluster_id)
    ]

    if result.empty:
        return f"Cluster {cluster_id}"

    if "Suggested Cluster Name" in result.columns:

        return str(
            result.iloc[0]["Suggested Cluster Name"]
        )

    return f"Cluster {cluster_id}"


def format_number(value, decimals=2):

    try:
        return f"{float(value):.{decimals}f}"

    except (ValueError, TypeError):
        return "N/A"


def get_student_matches(student_id):

    return matches[
        matches["student_id"].astype(str)
        == str(student_id)
    ].copy()



def light_table(df, **kwargs):

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        **kwargs
    )



# ============================================================
# 7. SIDEBAR NAVIGATION
# ============================================================


with st.sidebar:

    st.markdown("## 🎓 SkillMatch AI")
    st.caption("STUDENT INTELLIGENCE PLATFORM")

    st.divider()

    st.markdown("### WORKSPACE")

    page = st.radio(
        "Navigate",
        [
            "Overview",
            "Student Analysis",
            "Company Matching",
            "Skill Recommendations"
        ],
        label_visibility="collapsed"
    )

    st.divider()

    st.markdown("### PROJECT INFORMATION")

    st.markdown("**SkillMatch AI**")
    st.caption(
        "Student Skill-Based Clustering "
        "and Company Mapping"
    )

    st.info("Machine Learning Prototype · Version 1.0")

    st.divider()

    st.caption("Python · Scikit-learn · Streamlit")



# ============================================================
# 8. MAIN HEADER
# ============================================================


st.markdown(
    """
    <div style="color:#246B50;
                font-size:11px;
                font-weight:700;
                letter-spacing:2px;">
        STUDENT CAREER INTELLIGENCE
    </div>
    """,
    unsafe_allow_html=True
)

st.title("SkillMatch AI")

st.markdown(
    "Discover skill patterns. Explore career opportunities. "
    "Build stronger profiles."
)

st.divider()

# ============================================================
# 9. OVERVIEW
# ============================================================

if page == "Overview":

    st.subheader("Platform Overview")

    st.caption(
        "A snapshot of student skill profiles and matching activity."
    )

    total_students = len(students)
    total_clusters = students["cluster"].nunique()
    total_companies = companies["company"].nunique()
    total_comparisons = len(matches)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Students Analysed",
        f"{total_students:,}"
    )

    col2.metric(
        "Skill Clusters",
        total_clusters
    )

    col3.metric(
        "Companies / Templates",
        total_companies
    )

    col4.metric(
        "Role Comparisons",
        f"{total_comparisons:,}"
    )

    st.markdown("")
    st.markdown("### Student Skill Distribution")

    left, right = st.columns([1.1, 1])

    # CLUSTER CHART

    with left:

        cluster_counts = (
            students["cluster"]
            .value_counts()
            .sort_index()
            .reset_index()
        )

        cluster_counts.columns = [
            "Cluster",
            "Students"
        ]

        cluster_counts["Cluster Name"] = (
            cluster_counts["Cluster"]
            .apply(get_cluster_name)
        )

        fig = px.bar(
            cluster_counts,
            x="Cluster Name",
            y="Students",
            color="Cluster Name",
            text="Students",
            color_discrete_sequence=[
                "#246B50",
                "#72947D",
                "#A9B9A5",
                "#C7B88A"
            ],
            title="Students across skill clusters"
        )

        fig.update_layout(
            showlegend=False,
            plot_bgcolor="#FFFFFF",
            paper_bgcolor="#FFFFFF",
            font_color="#202522",
            margin=dict(l=10, r=10, t=50, b=10),
            xaxis_title="",
            yaxis_title="Number of students"
        )

        fig.update_traces(
            textposition="outside"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # CATEGORY CHART

    with right:

        if available_categories:

            category_means = (
                profiles[available_categories]
                .mean()
                .reset_index()
            )

            category_means.columns = [
                "Skill Category",
                "Average Score"
            ]

            fig = px.bar(
                category_means,
                x="Average Score",
                y="Skill Category",
                orientation="h",
                text_auto=".2f",
                color_discrete_sequence=["#246B50"],
                title="Average cluster skill scores"
            )

            fig.update_layout(
                plot_bgcolor="#FFFFFF",
                paper_bgcolor="#FFFFFF",
                font_color="#202522",
                margin=dict(l=10, r=10, t=50, b=10),
                xaxis_range=[0, 5],
                xaxis_title="Average skill level",
                yaxis_title=""
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.info(
                "Skill category columns were not found."
            )

    st.markdown("---")

    st.markdown("### Explore Student Groups")

    for cluster_id in sorted(
        students["cluster"].dropna().unique()
    ):

        group = students[
            students["cluster"] == cluster_id
        ]

        cluster_name = get_cluster_name(cluster_id)

        with st.expander(
            f"Cluster {cluster_id} · {cluster_name}"
        ):

            a, b, c = st.columns(3)

            a.metric(
                "Students",
                len(group)
            )

            b.metric(
                "Average CGPA",
                format_number(group["cgpa"].mean())
            )

            c.metric(
                "Cluster",
                cluster_name
            )

            columns = [
                "student_id",
                "cgpa"
            ] + available_skills

            light_table(
                group[columns].head(10)
            )


# ============================================================
# 10. STUDENT ANALYSIS
# ============================================================

elif page == "Student Analysis":

    st.subheader("Student Analysis")

    st.caption(
        "Explore individual student profiles and skill strengths."
    )

    student_ids = sorted(
        students["student_id"].astype(str).unique()
    )

    selected_id = st.selectbox(
        "Search or select a student ID",
        student_ids
    )

    student = get_student(selected_id)

    if student is not None:

        cluster_name = get_cluster_name(
            student["cluster"]
        )

        a, b, c = st.columns(3)

        a.metric(
            "Student ID",
            str(student["student_id"])
        )

        b.metric(
            "CGPA",
            format_number(student["cgpa"])
        )

        c.metric(
            "Skill Cluster",
            cluster_name
        )

        st.markdown("---")

        st.markdown("### Individual Skill Profile")

        skill_values = pd.DataFrame({
            "Skill": available_skills,
            "Level": [
                float(student[skill])
                for skill in available_skills
            ]
        })

        fig = px.bar(
            skill_values,
            x="Skill",
            y="Level",
            color="Level",
            color_continuous_scale=[
                "#DCE6DC",
                "#72947D",
                "#246B50"
            ],
            range_y=[0, 5],
            title=f"Skill levels for {selected_id}"
        )

        fig.update_layout(
            plot_bgcolor="#FFFFFF",
            paper_bgcolor="#FFFFFF",
            font_color="#202522",
            coloraxis_showscale=False,
            xaxis_title="",
            yaxis_title="Skill level (0–5)",
            margin=dict(l=10, r=10, t=50, b=10)
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.markdown("### Skill Level Details")

        light_table(
            skill_values.sort_values(
                "Level",
                ascending=False
            )
        )

        st.markdown("### Student Profile Summary")

        strongest = skill_values.nlargest(
            3, "Level"
        )

        weakest = skill_values.nsmallest(
            3, "Level"
        )

        left, right = st.columns(2)

        with left:

            st.markdown("**Top strengths**")

            for _, row in strongest.iterrows():

                st.success(
                    f"{row['Skill'].replace('_', ' ').title()}: "
                    f"{row['Level']:.1f}/5"
                )

        with right:

            st.markdown("**Skills to develop**")

            for _, row in weakest.iterrows():

                st.warning(
                    f"{row['Skill'].replace('_', ' ').title()}: "
                    f"{row['Level']:.1f}/5"
                )


# ============================================================
# 11. COMPANY MATCHING
# ============================================================

elif page == "Company Matching":

    st.subheader("Company & Role Matching")

    st.caption(
        "Compare a student's skills against illustrative job-role requirements."
    )

    student_ids = sorted(
        students["student_id"].astype(str).unique()
    )

    selected_id = st.selectbox(
        "Select student",
        student_ids,
        key="matching_student"
    )

    student = get_student(selected_id)

    student_matches = get_student_matches(
        selected_id
    )

    if student is not None and not student_matches.empty:

        student_matches["match_percentage"] = pd.to_numeric(
            student_matches["match_percentage"],
            errors="coerce"
        )

        student_matches = student_matches.dropna(
            subset=["match_percentage"]
        )

        st.markdown("### Matching Filters")

        f1, f2, f3 = st.columns(3)

        with f1:

            company_options = ["All"] + sorted(
                student_matches["company"]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )

            selected_company = st.selectbox(
                "Company",
                company_options
            )

        with f2:

            role_options = ["All"] + sorted(
                student_matches["job_role"]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )

            selected_role = st.selectbox(
                "Job Role",
                role_options
            )

        with f3:

            min_match = st.slider(
                "Minimum Match Percentage",
                min_value=0,
                max_value=100,
                value=0
            )

        filtered = student_matches.copy()

        if selected_company != "All":

            filtered = filtered[
                filtered["company"] == selected_company
            ]

        if selected_role != "All":

            filtered = filtered[
                filtered["job_role"] == selected_role
            ]

        filtered = filtered[
            filtered["match_percentage"] >= min_match
        ]

        filtered = filtered.sort_values(
            "match_percentage",
            ascending=False
        )

        best_match = student_matches[
            "match_percentage"
        ].max()

        average_match = student_matches[
            "match_percentage"
        ].mean()

        a, b, c = st.columns(3)

        a.metric(
            "Best Skill Match",
            f"{best_match:.1f}%"
        )

        b.metric(
            "Average Match",
            f"{average_match:.1f}%"
        )

        c.metric(
            "Roles Displayed",
            len(filtered)
        )

        st.markdown("---")

        st.markdown("### Matching Opportunities")

        if "cgpa_eligible" in filtered.columns:

            filtered["CGPA Eligibility"] = (
                filtered["cgpa_eligible"]
                .astype(str)
                .str.lower()
                .map({
                    "true": "Yes",
                    "false": "No",
                    "1": "Yes",
                    "0": "No"
                })
                .fillna("Check data")
            )

        display_columns = [
            "company",
            "job_role",
            "match_percentage",
            "CGPA Eligibility",
            "missing_skills"
        ]

        display_columns = [
            column for column in display_columns
            if column in filtered.columns
        ]

        if not filtered.empty:

            light_table(
                filtered[display_columns],
                column_config={
                    "match_percentage":
                        st.column_config.ProgressColumn(
                            "Skill Match",
                            format="%.1f%%",
                            min_value=0,
                            max_value=100
                        )
                }
            )

            fig = px.bar(
                filtered.head(10),
                x="match_percentage",
                y="job_role",
                orientation="h",
                color="match_percentage",
                color_continuous_scale=[
                    "#DCE6DC",
                    "#72947D",
                    "#246B50"
                ],
                range_color=[0, 100],
                title="Top Matching Roles"
            )

            fig.update_layout(
                plot_bgcolor="#FFFFFF",
                paper_bgcolor="#FFFFFF",
                font_color="#202522",
                coloraxis_showscale=False,
                xaxis_title="Skill Match Percentage",
                yaxis_title="",
                xaxis_range=[0, 100],
                margin=dict(l=10, r=10, t=50, b=10)
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.info(
                "No roles match your filters. "
                "Try lowering the minimum match percentage."
            )

        st.caption(
            "Skill match is a measure of similarity to the listed role "
            "requirements, not a hiring probability. CGPA eligibility "
            "uses illustrative template thresholds."
        )

    else:

        st.warning(
            "No matching records found for this student."
        )


# ============================================================
# 12. SKILL RECOMMENDATIONS
# ============================================================

elif page == "Skill Recommendations":

    st.subheader("Personalised Skill Development")

    st.caption(
        "Identify improvement areas and explore recommendations."
    )

    student_ids = sorted(
        students["student_id"].astype(str).unique()
    )

    selected_id = st.selectbox(
        "Select student",
        student_ids,
        key="recommendation_student"
    )

    student = get_student(selected_id)

    student_recommendations = recommendations[
        recommendations["student_id"].astype(str)
        == str(selected_id)
    ].copy()

    if student is not None:

        a, b = st.columns(2)

        a.metric(
            "Current CGPA",
            format_number(student["cgpa"])
        )

        b.metric(
            "Skill Cluster",
            get_cluster_name(student["cluster"])
        )

        st.markdown("---")

        if student_recommendations.empty:

            st.success(
                "No skill development recommendations "
                "were generated for this student."
            )

        else:

            st.markdown("### Recommended Areas to Improve")

            st.caption(
                "These recommendations come from the existing "
                "skill-gap recommendation engine."
            )

            light_table(
                student_recommendations
            )

            # Allow selection of a skill column even if its
            # column name is not exactly 'skill'.

            skill_column = next(
                (
                    column
                    for column in student_recommendations.columns
                    if column.lower() in [
                        "skill",
                        "skill_name",
                        "missing_skill"
                    ]
                ),
                None
            )

            if skill_column:

                skill_options = sorted(
                    student_recommendations[skill_column]
                    .dropna()
                    .astype(str)
                    .unique()
                )

                if skill_options:

                    selected_skill = st.selectbox(
                        "Explore a recommended skill",
                        skill_options
                    )

                    st.markdown("### Development Focus")

                    st.info(
                        "Focus area: "
                        + selected_skill.replace("_", " ").title()
                    )

                    selected_details = (
                        student_recommendations[
                            student_recommendations[
                                skill_column
                            ].astype(str) == selected_skill
                        ]
                    )

                    light_table(
                        selected_details
                    )

        st.markdown("---")

        st.markdown("### Current Skill Profile")

        current_skills = pd.DataFrame({
            "Skill": available_skills,
            "Level": [
                float(student[skill])
                for skill in available_skills
            ]
        })

        fig = px.bar(
            current_skills.sort_values(
                "Level",
                ascending=True
            ),
            x="Level",
            y="Skill",
            orientation="h",
            color_discrete_sequence=["#246B50"],
            range_x=[0, 5],
            title="Current Skill Levels"
        )

        fig.update_layout(
            plot_bgcolor="#FFFFFF",
            paper_bgcolor="#FFFFFF",
            font_color="#202522",
            xaxis_title="Skill level (0–5)",
            yaxis_title="",
            margin=dict(l=10, r=10, t=50, b=10)
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )



# ============================================================
# 13. FOOTER
# ============================================================

st.divider()

footer_left, footer_right = st.columns(2)

with footer_left:
    st.caption("SkillMatch AI · Student Career Intelligence")

with footer_right:
    st.caption(
        "Built with Python, Machine Learning & Streamlit"
    )
