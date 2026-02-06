"""
Curriculum Optimization - Professor Tool
"""
import streamlit as st
import json
from src.llm.client import GeminiClient
from src.llm.scenario_prompts import get_curriculum_optimization_prompt

st.set_page_config(page_title="Curriculum Optimization", page_icon="⚙️", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} [data-testid="stSidebar"] {display: none;}
    .stApp { background: #f7f7f8; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif; }
    .stButton>button { background: white; color: #202123; border: 1px solid #d9d9e3; border-radius: 6px; padding: 0.75rem 1.5rem; width: 100%; }
</style>
""", unsafe_allow_html=True)

if st.button("← Back to Dashboard"):
    st.switch_page("pages/Professor_Dashboard.py")

st.title("⚙️ Curriculum Optimization")
st.caption("Get data-driven recommendations to optimize your curriculum structure")

with st.form("curriculum_optimization_form"):
    st.markdown("### Current Curriculum")
    
    program_name = st.text_input("Program Name", placeholder="e.g., M.Tech in Data Science")
    
    current_structure = st.text_area(
        "Current Curriculum Structure",
        placeholder="Describe semesters, courses, credit distribution, prerequisites...",
        height=150
    )
    
    st.markdown("### Optimization Goals")
    
    optimization_goals = st.multiselect(
        "What do you want to optimize?",
        ["Learning Progression", "Credit Distribution", "Prerequisite Flow", 
         "Industry Alignment", "Student Workload Balance", "Skill Coverage", 
         "Time to Competency", "Elective Flexibility"],
        default=["Learning Progression"]
    )
    
    constraints = st.text_area(
        "Constraints (Optional)",
        placeholder="e.g., Total credits must be 120, Must include mandatory lab courses, Maximum 6 courses per semester...",
        height=80
    )
    
    pain_points = st.text_area(
        "Current Pain Points (Optional)",
        placeholder="e.g., Students struggle with certain course sequences, Heavy workload in semester 3...",
        height=80
    )
    
    submitted = st.form_submit_button("Generate Optimization Plan", use_container_width=True)

if submitted and program_name and current_structure:
    prompt = get_curriculum_optimization_prompt(
        program_name=program_name,
        current_structure=current_structure,
        optimization_goals=", ".join(optimization_goals),
        constraints=constraints if constraints else None,
        pain_points=pain_points if pain_points else None
    )
    
    with st.spinner("Analyzing and optimizing curriculum..."):
        try:
            llm_client = GeminiClient()
            response = llm_client.generate_with_retry(prompt=prompt, temperature=0.5)
            
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
            
            optimization = json.loads(json_str)
            st.session_state['optimization'] = optimization
            st.success("Optimization plan generated!")
        except Exception as e:
            st.error(f"Optimization failed: {str(e)}")

if 'optimization' in st.session_state:
    optimization = st.session_state['optimization']
    
    st.markdown("---")
    st.markdown("## Curriculum Optimization Report")
    
    if 'current_analysis' in optimization:
        with st.expander("📊 Current Curriculum Analysis", expanded=True):
            analysis = optimization['current_analysis']
            if isinstance(analysis, dict):
                for key, value in analysis.items():
                    st.markdown(f"**{key.replace('_', ' ').title()}:** {value}")
            else:
                st.markdown(analysis)
    
    if 'optimization_recommendations' in optimization:
        with st.expander("💡 Optimization Recommendations"):
            for rec in optimization['optimization_recommendations']:
                st.markdown(f"### {rec.get('area', '')}")
                st.markdown(f"**Current Issue:** {rec.get('current_issue', '')}")
                st.markdown(f"**Recommendation:** {rec.get('recommendation', '')}")
                st.caption(f"Impact: {rec.get('expected_impact', '')} | Effort: {rec.get('implementation_effort', '')}")
                st.markdown("---")
    
    if 'proposed_structure' in optimization:
        with st.expander("📋 Proposed Curriculum Structure"):
            for semester in optimization['proposed_structure']:
                st.markdown(f"### {semester.get('semester', '')}")
                if semester.get('courses'):
                    for course in semester['courses']:
                        st.markdown(f"- **{course.get('name', '')}** ({course.get('credits', '')} credits)")
                    st.caption(f"Total: {semester.get('total_credits', '')} credits")
                st.markdown("")
    
    if 'prerequisite_flow' in optimization:
        with st.expander("🔗 Improved Prerequisite Flow"):
            for flow in optimization['prerequisite_flow']:
                st.markdown(f"**{flow.get('course', '')}**")
                st.markdown(f"Prerequisites: {', '.join(flow.get('prerequisites', []))}")
                st.markdown(f"Enables: {', '.join(flow.get('enables', []))}")
                st.markdown("")
    
    if 'implementation_plan' in optimization:
        with st.expander("🚀 Implementation Plan"):
            for phase in optimization['implementation_plan']:
                st.markdown(f"**Phase {phase.get('phase', '')}:** {phase.get('title', '')}")
                st.markdown(f"Timeline: {phase.get('timeline', '')}")
                if phase.get('actions'):
                    st.markdown("Actions:")
                    for action in phase['actions']:
                        st.markdown(f"  - {action}")
                st.markdown("")
    
    st.markdown("---")
    st.download_button(
        label="Download Optimization Report (JSON)",
        data=json.dumps(optimization, indent=2),
        file_name="curriculum_optimization.json",
        mime="application/json",
        use_container_width=True
    )
