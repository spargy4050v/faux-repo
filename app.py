"""
CurricuLab AI - Intelligent Curriculum Design Platform
Landing page with role selection
"""
import streamlit as st

# Page configuration
st.set_page_config(
    page_title="CurricuLab AI",
    page_icon="📚",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Minimalistic CSS
st.markdown("""
<style>
    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stSidebar"] {display: none;}
    
    /* Clean styling */
    .stApp {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
        background: #f7f7f8;
    }
    
    .main .block-container {
        padding-top: 3rem;
        max-width: 700px;
    }
    
    .app-title {
        text-align: center;
        font-size: 2.5rem;
        font-weight: 600;
        color: #202123;
        margin-bottom: 0.5rem;
    }
    
    .app-subtitle {
        text-align: center;
        font-size: 1rem;
        color: #6e6e80;
        margin-bottom: 4rem;
    }
    
    .role-label {
        font-size: 0.875rem;
        color: #6e6e80;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    
    .stButton>button {
        background: white;
        color: #202123;
        border: 1px solid #d9d9e3;
        border-radius: 6px;
        padding: 0.875rem 1.5rem;
        font-weight: 500;
        font-size: 0.95rem;
        width: 100%;
        transition: all 0.2s;
    }
    
    .stButton>button:hover {
        background: #f7f7f8;
        border-color: #c5c5d2;
        transform: scale(1.02);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'role' not in st.session_state:
    st.session_state['role'] = None

# Header
st.markdown('<h1 class="app-title">CurricuLab AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="app-subtitle">Intelligent Curriculum Design Platform</p>', unsafe_allow_html=True)

# Role Selection Section
st.markdown('<p class="role-label">Select Your Role</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="medium")

with col1:
    if st.button("Student", use_container_width=True):
        st.session_state['role'] = 'student'
        st.switch_page("pages/Student_Dashboard.py")

with col2:
    if st.button("Professor", use_container_width=True):
        st.session_state['role'] = 'professor'
        st.switch_page("pages/Professor_Dashboard.py")
