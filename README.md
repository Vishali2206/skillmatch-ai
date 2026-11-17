# Student Skill-Based Clustering and Company Mapping

Beginner-friendly Python + K-Means + Streamlit project.

## Important dataset note
- `students_synthetic.csv` contains 200 generated demonstration records. They are NOT real student records.
- `company_roles_template.csv` contains illustrative role/skill templates. It is NOT a verified list of current vacancies or official eligibility criteria. Before final submission, replace/verify each role's requirements using official company career pages or current job descriptions and paste the source URL.

## Project structure
- `data/`: CSV datasets
- `app.py`: Streamlit dashboard (added in the next build step)
- `requirements.txt`: Python packages
- `README.md`: instructions

## Setup (Windows)
1. Install Python 3.11 or 3.12 from https://www.python.org/downloads/
2. During installation, tick **Add Python to PATH**.
3. Extract the ZIP folder.
4. Open the folder in VS Code.
5. Open Terminal > New Terminal.
6. Create a virtual environment:
   `py -m venv .venv`
7. Activate it:
   PowerShell: `.venv\Scripts\Activate.ps1`
   If PowerShell blocks activation, use Command Prompt: `.venv\Scripts\activate.bat`
8. Install packages:
   `py -m pip install -r requirements.txt`

## Run (after app.py is added)
`py -m streamlit run app.py`

## Suggested two-person division
- Member 1: dataset preparation, company-source verification, data cleaning.
- Member 2: K-Means implementation, dashboard, visualizations and testing.
- Both: viva preparation, validation and final presentation.

## Ethical note
Use synthetic records for development. Use real student data only with college permission, informed consent where required, and remove direct identifiers.
# skillmatch-ai
Student Skill-Based Clustering and Company Mapping using Python, Machine Learning and Streamlit.
