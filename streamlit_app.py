import streamlit as st
import pandas as pd
import os
import plotly.express as px


job_listings = pd.read_excel(os.path.join('data', 'May 28, Cleaned Roles.xlsx'))

# --- SIDEBAR FILTERS ---
st.sidebar.title("Filters")

# Industry filter
selected_industries = st.sidebar.multiselect("Industry", job_listings["IQ_INDUSTRY_CLASSIFICATION"].unique(), default=job_listings["IQ_INDUSTRY_CLASSIFICATION"].unique())

# Job Function filter
selected_functions = st.sidebar.multiselect("Job Function", job_listings["job_function"].unique(), default=job_listings["job_function"].unique())  # Default to all skills selected

# Location filter
selected_locations = st.sidebar.multiselect("Location", list(job_listings["location"].unique()) + ['All'], default='All')
print(selected_locations)

# Experience Level filter
#selected_experience = st.sidebar.multiselect("Experience Level", job_listings["experience_level"].unique())

# Keyword Search
search_term = st.sidebar.text_input("Keyword Search")

# Apply Filters
filtered_jobs = job_listings[
    job_listings["IQ_INDUSTRY_CLASSIFICATION"].isin(selected_industries) &
    job_listings["job_function"].isin(selected_functions) &
    job_listings["location"].isin(job_listings["location"].unique() if 'All' in selected_locations else selected_locations) &
    #job_data["experience_level"].isin(selected_experience) &
    job_listings["Standardized Role"].str.lower().str.contains(search_term.lower(), na=False)  # Case-insensitive search
]
#filtered_companies = top_companies_data[top_companies_data["IQ_INDUSTRY_CLASSIFICATION"].isin(selected_industries)]

top_companies_data = filtered_jobs.groupby('Company').count()['title'].reset_index()
top_companies_data.columns = ['Company', 'Open Positions']
top_companies_data = top_companies_data.sort_values(by='Open Positions', ascending=False)

top_companies_data = pd.merge(top_companies_data, filtered_jobs[['Company', 'IQ_INDUSTRY_CLASSIFICATION', 'IQ_INDUSTRY_GROUP']].drop_duplicates('Company'), how='left', left_on='Company', right_on='Company')


top_companies_data_via_imp_score = filtered_jobs.groupby('Company').mean('Combined Normalized Industry Importance and Overall % from Motivations').reset_index()[['Company', 'Combined Normalized Industry Importance and Overall % from Motivations']]
top_companies_data_via_imp_score.columns = ['Company', 'Score']
top_companies_data_via_imp_score = top_companies_data_via_imp_score.sort_values(by='Score', ascending=False)

top_companies_data_via_imp_score = pd.merge(top_companies_data_via_imp_score, filtered_jobs[['Company', 'IQ_INDUSTRY_CLASSIFICATION', 'IQ_INDUSTRY_GROUP']].drop_duplicates('Company'), how='left', left_on='Company', right_on='Company')
top_companies_data_via_imp_score = pd.merge(top_companies_data_via_imp_score, top_companies_data[['Company', 'Open Positions',]], how='left',  left_on='Company', right_on='Company')

top_companies_data_via_imp_score = top_companies_data_via_imp_score[top_companies_data_via_imp_score['Open Positions']>=3].reset_index(drop=True)


# --- MAIN CONTENT ---
st.title("Job Insights Dashboard")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["Top Companies", "Market Demand", "Trending Skills", "Industry Insights"])

# Tab 1: Top Companies
with tab1:
    st.subheader("Top Companies for Your Students")
    # ... (Implement your ranking algorithm here to order filtered_companies)

    for index, row in top_companies_data_via_imp_score.iterrows():
        with st.container():
            st.write(f"**{index+1}. {row['Company']}**")
            col1, col2, col3 = st.columns(3)  # Divide the row into three columns for better layout
            with col1:
                st.write(f"**Industry:** {row['IQ_INDUSTRY_CLASSIFICATION']}")
            with col2:
                st.write(f"**Open Positions:** {row['Open Positions']}")
            #with col3:
            #    st.write(f"**Experience Level:** {row['Experience Level']}")
            #if row['Alumni Connections'] == 'Yes':  # Display alumni connection if applicable
            #    st.write("**Alumni Connection:** ✅")
            #else:
            #    st.write("**Alumni Connection:** ❌")  # Display a cross mark if no connection
            # st.write(row['Company Name'])  # Display the company description
            st.button("Contact", key=row['Company'])  # Placeholder for a contact button

##tab2: Market Demand
with tab2:
    st.subheader("Current Market Demand")
    # ... (Implement your ranking algorithm here to order filtered_companies)

    for index, row in top_companies_data.iterrows():
        with st.container():
            st.write(f"**{index+1}. {row['Company']}**")
            col1, col2, col3 = st.columns(3)  # Divide the row into three columns for better layout
            with col1:
                st.write(f"**Industry:** {row['IQ_INDUSTRY_CLASSIFICATION']}")
            with col2:
                st.write(f"**Open Positions:** {row['Open Positions']}")
            #with col3:
            #    st.write(f"**Experience Level:** {row['Experience Level']}")
            #if row['Alumni Connections'] == 'Yes':  # Display alumni connection if applicable
            #    st.write("**Alumni Connection:** ✅")
            #else:
            #    st.write("**Alumni Connection:** ❌")  # Display a cross mark if no connection
            # st.write(row['Company Name'])  # Display the company description
            st.button("Contact", key=index)  # Placeholder for a contact button

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

with tab3:
    st.subheader("Trending Skills")
    # Create your Plotly charts here (using skill_trends_data and top_skills_data)


## Tab 4 industry insights
industry_counts = job_listings.groupby('IQ_INDUSTRY_CLASSIFICATION').count()['title'].reset_index()
industry_counts.columns = ['Industry', 'Open Positions']
industry_counts = industry_counts.sort_values(by='Open Positions', ascending=False)

fig = px.bar(
    industry_counts,
    x='Industry',
    y='Open Positions',
    title='Open Positions by Industry',
    color='Industry',
    color_discrete_sequence=px.colors.qualitative.Vivid,
    text='Open Positions',
    hover_data={'Industry': True, 'Open Positions': True}
)

fig.update_layout(
    title={
        'text': 'Open Positions by Industry',
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    xaxis_title='Industry',
    yaxis_title='Open Positions',
    uniformtext_minsize=8,
    uniformtext_mode='hide',
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(
        family="Arial, sans-serif",
        size=12,
        color="#7f7f7f"
    ),
    hoverlabel=dict(
        bgcolor="white",
        font_size=13,
        font_family="Arial, sans-serif"
    ),
    yaxis=dict(
        title='Open Positions',
        titlefont=dict(size=14),
        tickfont=dict(size=12)
    ),
    xaxis=dict(
        title='Industry',
        titlefont=dict(size=14),
        tickfont=dict(size=12)
    )
)

with tab4:
    st.subheader("Industry Insights")

    st.plotly_chart(fig)
    # Create your Plotly charts here (using industry_data and industry_dist_data)
