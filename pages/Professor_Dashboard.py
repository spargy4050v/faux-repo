"""
Professor Dashboard - All Tools
"""
import streamlit as st

st.set_page_config(
    page_title="Professor Dashboard",
    page_icon="👨‍🏫",
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
st.markdown('<h1 class="header-title">Professor Dashboard</h1>', unsafe_allow_html=True)
st.markdown('<p class="header-subtitle">Design and optimize academic curricula</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

if st.button("← Back to Home"):
    st.switch_page("app.py")

st.markdown("### Select a Tool")

# Tools grid
col1, col2, col3 = st.columns(3, gap="large")

with col1:
    if st.button("📚 Course Structure Generator", key="course_structure", use_container_width=True, help="Generate comprehensive course structures"):
        st.switch_page("pages/Professor_Course_Structure_Generator.py")
    
    if st.button("🔄 Curriculum Optimization", key="curriculum_opt", use_container_width=True, help="Optimize existing curricula"):
        st.switch_page("pages/Professor_Curriculum_Optimization.py")

with col2:
    if st.button("🎯 Learning Outcome Mapping", key="outcome_mapping", use_container_width=True, help="Map content to learning outcomes"):
        st.switch_page("pages/Professor_Learning_Outcome_Mapping.py")
    
    if st.button("📊 Topic Recommendations", key="topic_rec", use_container_width=True, help="Get AI-powered topic suggestions"):
        st.switch_page("pages/Professor_Topic_Recommendations.py")

with col3:
    if st.button("💼 Industry Alignment Analysis", key="industry_align", use_container_width=True, help="Align with industry demands"):
        st.switch_page("pages/Professor_Industry_Alignment_Analysis.py")
    
    if st.button("🔗 Prerequisite Analysis", key="prereq", use_container_width=True, help="Structure course prerequisites"):
        st.switch_page("pages/Professor_Prerequisite_Analysis.py")
