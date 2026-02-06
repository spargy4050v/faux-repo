"""
Prerequisite Analysis - Professor Tool
"""
import streamlit as st
import json
from src.llm.client import GeminiClient
from src.llm.scenario_prompts import get_prerequisite_analysis_prompt

st.set_page_config(page_title="Prerequisite Analysis", page_icon="🔗", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} [data-testid="stSidebar"] {display: none;}
    .stApp { background: #f7f7f8; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif; }
    .stButton>button { background: white; color: #202123; border: 1px solid #d9d9e3; border-radius: 6px; padding: 0.75rem 1.5rem; width: 100%; }
</style>
""", unsafe_allow_html=True)

if st.button("← Back to Dashboard"):
    st.switch_page("pages/Professor_Dashboard.py")

st.title("🔗 Prerequisite Analysis")
st.caption("Analyze and optimize course prerequisites and dependencies")

with st.form("prerequisite_analysis_form"):
    st.markdown("### Course to Analyze")
    
    course_name = st.text_input("Course Name", placeholder="e.g., Machine Learning")
    
    course_topics = st.text_area(
        "Major Topics in This Course",
        placeholder="List the key topics and concepts covered...",
        height=120
    )
    
    st.markdown("### Current Prerequisites")
    
    current_prerequisites = st.text_area(
        "Current Prerequisite Courses",
        placeholder="List courses currently listed as prerequisites...",
        height=80
    )
    
    st.markdown("### Program Context")
    
    available_courses = st.text_area(
        "Other Courses in Program",
        placeholder="List other related courses in your program that could be prerequisites or follow-up courses...",
        height=100
    )
    
    analysis_type = st.multiselect(
        "Analysis Goals",
        ["Identify missing prerequisites", "Remove unnecessary prerequisites", 
         "Suggest optimal prerequisite chain", "Identify corequisites", 
         "Analyze prerequisite gaps"],
        default=["Identify missing prerequisites"]
    )
    
    submitted = st.form_submit_button("Analyze Prerequisites", use_container_width=True)

if submitted and course_name and course_topics:
    prompt = get_prerequisite_analysis_prompt(
        course_name=course_name,
        course_topics=course_topics,
        current_prerequisites=current_prerequisites if current_prerequisites else "None specified",
        available_courses=available_courses if available_courses else None,
        analysis_goals=", ".join(analysis_type)
    )
    
    with st.spinner("Analyzing prerequisite structure..."):
        try:
            llm_client = GeminiClient()
            response = llm_client.generate_with_retry(prompt=prompt, temperature=0.4)
            
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
            st.session_state['prerequisite_analysis'] = analysis
            st.success("Prerequisite analysis complete!")
        except Exception as e:
            st.error(f"Analysis failed: {str(e)}")

if 'prerequisite_analysis' in st.session_state:
    analysis = st.session_state['prerequisite_analysis']
    
    st.markdown("---")
    st.markdown("## Prerequisite Analysis Report")
    
    if 'required_prerequisites' in analysis:
        with st.expander("✅ Recommended Prerequisites", expanded=True):
            for prereq in analysis['required_prerequisites']:
                importance = prereq.get('importance', '')
                emoji = "🔴" if importance == "Critical" else "🟡" if importance == "Important" else "🟢"
                st.markdown(f"{emoji} **{prereq.get('course', '')}**")
                st.markdown(f"**Rationale:** {prereq.get('rationale', '')}")
                if prereq.get('concepts_needed'):
                    st.caption(f"Key Concepts: {', '.join(prereq['concepts_needed'])}")
                st.markdown("")
    
    if 'missing_prerequisites' in analysis:
        with st.expander("⚠️ Missing Prerequisites"):
            for missing in analysis['missing_prerequisites']:
                st.markdown(f"**{missing.get('prerequisite', '')}**")
                st.markdown(f"Why needed: {missing.get('reason', '')}")
                st.caption(f"Impact of not having: {missing.get('impact', '')}")
                if missing.get('alternative'):
                    st.info(f"Alternative: {missing['alternative']}")
                st.markdown("---")
    
    if 'unnecessary_prerequisites' in analysis:
        with st.expander("➖ Potentially Unnecessary Prerequisites"):
            for unnecessary in analysis['unnecessary_prerequisites']:
                st.markdown(f"**{unnecessary.get('course', '')}**")
                st.markdown(f"Reason: {unnecessary.get('reason', '')}")
                st.markdown("")
    
    if 'corequisites' in analysis:
        with st.expander("🔄 Suggested Corequisites"):
            for coreq in analysis['corequisites']:
                st.markdown(f"**{coreq.get('course', '')}**")
                st.markdown(f"Benefit: {coreq.get('benefit', '')}")
                st.markdown("")
    
    if 'prerequisite_chain' in analysis:
        with st.expander("🔗 Complete Prerequisite Chain"):
            for level in analysis['prerequisite_chain']:
                st.markdown(f"**Level {level.get('level', '')}:** {level.get('description', '')}")
                if level.get('courses'):
                    st.markdown("Courses: " + ", ".join(level['courses']))
                st.markdown("")
    
    if 'knowledge_gaps' in analysis:
        with st.expander("📊 Identified Knowledge Gaps"):
            for gap in analysis['knowledge_gaps']:
                st.markdown(f"**Gap:** {gap.get('gap', '')}")
                st.markdown(f"Current Coverage: {gap.get('current_coverage', '')}")
                st.markdown(f"**Recommendation:** {gap.get('recommendation', '')}")
                st.markdown("---")
    
    st.markdown("---")
    st.download_button(
        label="Download Prerequisite Analysis (JSON)",
        data=json.dumps(analysis, indent=2),
        file_name="prerequisite_analysis.json",
        mime="application/json",
        use_container_width=True
    )
