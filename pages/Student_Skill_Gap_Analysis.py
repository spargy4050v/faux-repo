"""
Skill Gap Analysis - Student Tool
"""
import streamlit as st
import json
from src.llm.client import GeminiClient
from src.llm.scenario_prompts import get_skill_gap_analysis_prompt

st.set_page_config(page_title="Skill Gap Analysis", page_icon="📄", layout="centered", initial_sidebar_state="collapsed")

# CSS  
st.markdown("""
<style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} [data-testid="stSidebar"] {display: none;}
    .stApp { background: #f7f7f8; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif; }
    .stButton>button { background: white; color: #202123; border: 1px solid #d9d9e3; border-radius: 6px; padding: 0.75rem 1.5rem; width: 100%; }
</style>
""", unsafe_allow_html=True)

if st.button("← Back to Dashboard"):
    st.switch_page("pages/Student_Dashboard.py")

st.title("📄 Skill Gap Analysis")
st.caption("Identify skill gaps and get personalized learning recommendations")

# Form
with st.form("skill_gap_form"):
    st.markdown("### Your Information")
    
    resume_text = st.text_area(
        "Paste Your Resume or Skills Summary",
        placeholder="Include your education, work experience, technical skills, projects, etc.",
        height=200
    )
    
    st.markdown("### Target Role (Optional)")
    target_role = st.text_input("Desired Job Title", placeholder="e.g., Data Scientist, Full Stack Developer")
    
    job_description = st.text_area(
        "Job Description (Optional)",
        placeholder="Paste a job description you're targeting...",
        height=150
    )
    
    submitted = st.form_submit_button("Analyze Skill Gaps", use_container_width=True)

if submitted and resume_text:
    prompt = get_skill_gap_analysis_prompt(
        resume_text=resume_text,
        target_role=target_role if target_role else None,
        job_description=job_description if job_description else None
    )
    
    with st.spinner("Analyzing your skills and identifying gaps..."):
        try:
            llm_client = GeminiClient()
            response = llm_client.generate_with_retry(prompt=prompt, temperature=0.5)
            
            # Parse JSON
            json_str = response.strip()
            if "```json" in json_str:
                json_str = json_str.split("```json")[1].split("```")[0].strip()
            elif "```" in json_str:
                parts = json_str.split("```")
                if len(parts) >= 2:
                    json_str = parts[1].strip()
            
            if "{" in json_str and "}" in json_str:
                start = json_str.find("{")
                end = json_str.rfind("}") + 1
                json_str = json_str[start:end]
            
            analysis = json.loads(json_str)
            st.session_state['skill_analysis'] = analysis
            st.success("Skill analysis complete!")
        except Exception as e:
            st.error(f"Analysis failed: {str(e)}")

# Display Results
if 'skill_analysis' in st.session_state:
    analysis = st.session_state['skill_analysis']
    
    st.markdown("---")
    st.markdown("## Your Skill Analysis")
    
    # Current Skills
    if 'current_skills' in analysis:
        with st.expander("✅ Your Current Skills", expanded=True):
            for skill in analysis['current_skills']:
                st.markdown(f"**{skill.get('skill', '')}** - {skill.get('proficiency_level', '')}")
                if skill.get('evidence'):
                    st.caption(f"Evidence: {skill['evidence']}")
    
    # Skill Gaps
    if 'skill_gaps' in analysis:
        with st.expander("🎯 Skill Gaps to Address", expanded=True):
            for gap in analysis['skill_gaps']:
                importance = gap.get('importance', '')
                emoji = "🔴" if importance == "Critical" else "🟡" if importance == "High" else "🟢"
                st.markdown(f"{emoji} **{gap.get('skill', '')}** - {importance}")
                st.caption(f"Time to acquire: {gap.get('estimated_time', '')} | Difficulty: {gap.get('difficulty_to_acquire', '')}")
    
    # Learning Roadmap
    if 'learning_roadmap' in analysis:
        with st.expander("📚 Your Learning Roadmap"):
            for item in sorted(analysis['learning_roadmap'], key=lambda x: x.get('priority', 10), reverse=True):
                st.markdown(f"**Priority {item.get('priority', '')}: {item.get('skill', '')}**")
                st.markdown(f"*Estimated Duration: {item.get('estimated_duration', '')}*")
                
                if item.get('learning_path'):
                    st.markdown("Learning Path:")
                    for step in item['learning_path']:
                        st.markdown(f"  → {step}")
                
                if item.get('resources'):
                    st.markdown("Resources:")
                    for resource in item['resources']:
                        st.markdown(f"  - {resource}")
                st.markdown("---")
    
    # Strengths
    if 'strengths' in analysis:
        with st.expander("💪 Your Strengths"):
            for strength in analysis['strengths']:
                st.markdown(f"- {strength}")
    
    # Recommended Focus
    if 'recommended_focus' in analysis:
        st.markdown("#### 🎯 Recommended Focus Areas")
        cols = st.columns(min(len(analysis['recommended_focus']), 3))
        for idx, skill in enumerate(analysis['recommended_focus']):
            with cols[idx % 3]:
                st.info(skill)
    
    # Download
    st.markdown("---")
    st.download_button(
        label="Download Skill Analysis (JSON)",
        data=json.dumps(analysis, indent=2),
        file_name="skill_gap_analysis.json",
        mime="application/json",
        use_container_width=True
    )
