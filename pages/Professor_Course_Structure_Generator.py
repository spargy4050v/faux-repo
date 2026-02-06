"""
Course Structure Generator - Professor Tool
"""
import streamlit as st
import json
from src.llm.client import GeminiClient  
from src.llm.scenario_prompts import get_course_structure_prompt

st.set_page_config(page_title="Course Structure Generator", page_icon="📚", layout="centered", initial_sidebar_state="collapsed")

# CSS
st.markdown("""
<style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} [data-testid="stSidebar"] {display: none;}
    .stApp { background: #f7f7f8; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif; }
    .stButton>button { background: white; color: #202123; border: 1px solid #d9d9e3; border-radius: 6px; padding: 0.75rem 1.5rem; width: 100%; }
    .stButton>button:hover { background: #f7f7f8; }
</style>
""", unsafe_allow_html=True)

if st.button("← Back to Dashboard"):
    st.switch_page("pages/Professor_Dashboard.py")

st.title("📚 Course Structure Generator")
st.caption("Generate comprehensive course structures with topics, objectives, and assessments")

# Form
with st.form("course_structure_form"):
    course_name = st.text_input("Course Name", placeholder="e.g., Advanced Machine Learning")
    
    col1, col2 = st.columns(2)
    with col1:
        level = st.selectbox("Academic Level", ["Undergraduate", "Graduate", "Professional", "Certification"])
    with col2:
        duration = st.number_input("Duration (weeks)", min_value=4, max_value=20, value=12)
    
    prerequisites = st.text_area("Prerequisites (one per line)", placeholder="Linear Algebra\nProgramming Basics")
    focus_areas = st.text_area("Focus Areas (one per line)", placeholder="Deep Learning\nNLP\nComputer Vision")
    
    additional_notes = st.text_area("Additional Requirements (optional)", placeholder="Include hands-on projects, industry case studies, etc.")
    
    submitted = st.form_submit_button("Generate Course Structure", use_container_width=True)

if submitted and course_name:
    prereq_list = [p.strip() for p in prerequisites.split('\n') if p.strip()]
    focus_list = [f.strip() for f in focus_areas.split('\n') if f.strip()]
    
    prompt = get_course_structure_prompt(
        course_name=course_name,
        level=level,
        duration_weeks=duration,
        prerequisites=prereq_list,
        focus_areas=focus_list
    )
    
    if additional_notes:
        prompt += f"\n\nAdditional Requirements: {additional_notes}"
    
    with st.spinner(f"Generating comprehensive structure for {course_name}..."):
        try:
            llm_client = GeminiClient()
            response = llm_client.generate_with_retry(prompt=prompt, temperature=0.4)
            
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
            
            course_structure = json.loads(json_str)
            st.session_state['course_structure'] = course_structure
            st.success("Course structure generated successfully!")
        except Exception as e:
            st.error(f"Generation failed: {str(e)}")

# Display results
if 'course_structure' in st.session_state:
    structure = st.session_state['course_structure']
    
    st.markdown("---")
    st.markdown(f"### {structure.get('course_name', 'Course Structure')}")
    st.caption(f"Level: {structure.get('level', '')} | Duration: {structure.get('total_weeks', '')} weeks")
    
    # Weekly Structure
    if 'weekly_structure' in structure:
        st.markdown("#### Weekly Breakdown")
        for week in structure['weekly_structure']:
            with st.expander(f"Week {week.get('week', '')} - {', '.join(week.get('topics', [])[:2])}"):
                st.markdown(f"**Topics**: {', '.join(week.get('topics', []))}")
                st.markdown(f"**Learning Objectives**:")
                for obj in week.get('learning_objectives', []):
                    st.markdown(f"- {obj}")
                if week.get('activities'):
                    st.markdown(f"**Activities**: {', '.join(week.get('activities', []))}")
                if week.get('assessments'):
                    st.markdown(f"**Assessments**: {', '.join(week.get('assessments', []))}")
    
    # Course Outcomes
    if 'course_outcomes' in structure:
        with st.expander("Course Learning Outcomes"):
            for outcome in structure['course_outcomes']:
                st.markdown(f"- {outcome}")
    
    #Resources
    if 'recommended_resources' in structure:
        with st.expander("Recommended Resources"):
            for resource in structure['recommended_resources']:
                st.markdown(f"- {resource}")
    
    # Download
    st.markdown("---")
    st.download_button(
        label="Download Course Structure (JSON)",
        data=json.dumps(structure, indent=2),
        file_name=f"{course_name.replace(' ', '_')}_structure.json",
        mime="application/json",
        use_container_width=True
    )
