import streamlit as st
import pandas as pd
import plotly.express as px

# Mock data
job_data = pd.DataFrame({
    "title": ["Data Scientist", "Software Engineer", "Marketing Manager", "Financial Analyst"],
    "company": ["TechCorp", "Innovate Solutions", "Global Brands", "FinancePro"],
    "location": ["Hyderabad", "Bengaluru", "Mumbai", "Delhi"],
    "skills": ["Python, Machine Learning", "Java, SQL", "Digital Marketing, SEO", "Excel, Finance"],
    "industry": ["Technology", "IT Services", "Marketing", "Finance"],
    "experience_level": ["Entry-level", "Mid-level", "Entry-level", "Mid-level"]
})

company_data = pd.DataFrame({
    "company": ["TechCorp", "Innovate Solutions", "Global Brands", "FinancePro"],
    "industry": ["Technology", "IT Services", "Marketing", "Finance"],
    "open_positions": [3, 5, 2, 1],
    "description": ["Innovative tech company", "Leading IT solutions provider", "Global consumer brands", "Financial services firm"]
})


# --- SIDEBAR FILTERS ---
st.sidebar.title("Filters")

# Industry filter
selected_industries = st.sidebar.multiselect("Industry Sector", job_data["industry"].unique())

# Job Function filter
selected_functions = st.sidebar.multiselect("Job Function", job_data["skills"].unique(), default=job_data["skills"].unique())  # Default to all skills selected

# Location filter
selected_locations = st.sidebar.multiselect("Location", job_data["location"].unique())

# Experience Level filter
selected_experience = st.sidebar.multiselect("Experience Level", job_data["experience_level"].unique())

# Keyword Search
search_term = st.sidebar.text_input("Keyword Search")

# Apply Filters
filtered_jobs = job_data[
    job_data["industry"].isin(selected_industries) &
    job_data["skills"].isin(selected_functions) &
    job_data["location"].isin(selected_locations) &
    job_data["experience_level"].isin(selected_experience) &
    job_data["title"].str.lower().str.contains(search_term.lower(), na=False)  # Case-insensitive search
]
filtered_companies = company_data[company_data["industry"].isin(selected_industries)]

# --- MAIN CONTENT ---
st.title("Job Insights Dashboard")

# Tabs
tab1, tab2, tab3 = st.tabs(["Top Companies", "Trending Skills", "Industry Insights"])

# Tab 1: Top Companies

# Mock data for Top Companies tab
top_companies_data = pd.DataFrame({
    'Company Name': ['TechCorp', 'Innovate Solutions', 'Global Brands', 'FinancePro'],
    'Industry Sector': ['Technology', 'IT Services', 'Consumer Goods', 'Finance'],
    'Job Function(s)': ['Data Scientist, Software Engineer', 'Software Engineer, IT Consultant', 'Marketing Manager, Brand Analyst', 'Financial Analyst, Accountant'],
    'Open Positions': [5, 8, 3, 2],
    'Experience Level': ['Entry-level, Mid-level', 'Mid-level', 'Entry-level', 'Mid-level'],
    'Alumni Connections': ['Yes', 'No', 'Yes', 'No']
})

with tab1:
    st.subheader("Top Companies for Your Students")
    # ... (Implement your ranking algorithm here to order filtered_companies)

    for index, row in top_companies_data.iterrows():
        with st.container():
            st.write(f"**{index+1}. {row['Company Name']}**")
            col1, col2, col3 = st.columns(3)  # Divide the row into three columns for better layout
            with col1:
                st.write(f"**Industry:** {row['Industry Sector']}")
            with col2:
                st.write(f"**Open Positions:** {row['Open Positions']}")
            with col3:
                st.write(f"**Experience Level:** {row['Experience Level']}")
            if row['Alumni Connections'] == 'Yes':  # Display alumni connection if applicable
                st.write("**Alumni Connection:** ✅")
            else:
                st.write("**Alumni Connection:** ❌")  # Display a cross mark if no connection
            # st.write(row['Company Name'])  # Display the company description
            st.button("Contact", key=row['Company Name'])  # Placeholder for a contact button

# Tab 2: Trending Skills

skill_trends_data = pd.DataFrame({
    'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
    'Python': [50, 55, 62, 70, 78, 85],
    'SQL': [40, 42, 45, 50, 52, 55],
    'Data Analysis': [35, 38, 42, 48, 55, 60]
})
top_skills_data = pd.DataFrame({
    'Skill': ['Python', 'SQL', 'Data Analysis', 'Java', 'Project Management', 'Communication', 'Leadership', 'Marketing', 'Finance', 'Cloud Computing'],
    'Job Postings': [120, 90, 85, 75, 60, 55, 50, 45, 40, 35]
})

with tab2:
    st.subheader("Trending Skills")
    # Create your Plotly charts here (using skill_trends_data and top_skills_data)

# Tab 3: Industry Insights
industry_data = pd.DataFrame({
    'Industry': ['Technology', 'IT Services', 'Finance', 'Marketing', 'Healthcare', 'Consulting'],
    'Job Postings': [350, 280, 150, 120, 90, 60]
})
industry_dist_data = pd.DataFrame({
    'Industry': ['Technology', 'IT Services', 'Finance', 'Marketing', 'Healthcare', 'Consulting'],
    'Percentage': [35, 28, 15, 12, 9, 6]
})
with tab3:
    st.subheader("Industry Insights")
    # Create your Plotly charts here (using industry_data and industry_dist_data)
