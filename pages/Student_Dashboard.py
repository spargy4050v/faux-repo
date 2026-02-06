"""
Student Dashboard - All Tools
"""
import streamlit as st

st.set_page_config(
    page_title="Student Dashboard",
    page_icon="👨‍🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stSidebar"] {display: none;}
    
    .stApp {
        background: #f7f7f8;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
    }
    
    .dashboard-header {
        background: white;
        border-bottom: 1px solid #e5e5e5;
        padding: 1.5rem 0;
        margin-bottom: 2rem;
    }
    
    .header-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #202123;
        margin: 0;
    }
    
    .header-subtitle {
        font-size: 0.9rem;
        color: #6e6e80;
        margin-top: 0.25rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="dashboard-header">', unsafe_allow_html=True)
st.markdown('<h1 class="header-title">Student Dashboard</h1>', unsafe_allow_html=True)
st.markdown('<p class="header-subtitle">Your personalized career and learning hub</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

if st.button("← Back to Home"):
    st.switch_page("app.py")

st.markdown("### Select a Tool")

# Tools grid
col1, col2, col3 = st.columns(3, gap="large")

with col1:
    if st.button("📄 Skill Gap Analysis", key="skill_gap", use_container_width=True, help="Identify skill gaps and get recommendations"):
        st.switch_page("pages/Student_Skill_Gap_Analysis.py")
    
    if st.button("🎓 Course Prerequisites", key="prereq", use_container_width=True, help="Explore prerequisites for your career path"):
        st.switch_page("pages/Student_Course_Prerequisites.py")

with col2:
    if st.button("💼 Job Opportunities", key="jobs", use_container_width=True, help="Discover relevant job opportunities"):
        st.switch_page("pages/Student_Job_Opportunities.py")
    
    if st.button("💡 Project Ideas", key="projects", use_container_width=True, help="Get industry-relevant project ideas"):
        st.switch_page("pages/Student_Project_Ideas.py")

with col3:
    if st.button("📈 Career Path Planner", key="career", use_container_width=True, help="Map out your career trajectory"):
        st.switch_page("pages/Student_Career_Path_Planner.py")
    
    if st.button("🛠️ Industry Tools & Tech", key="tools", use_container_width=True, help="Stay updated with latest technologies"):
        st.switch_page("pages/Student_Industry_Tools.py")
