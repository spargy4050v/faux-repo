"""
Course Prerequisites - Student Tool
"""
import streamlit as st
import json
from src.llm.client import GeminiClient
from src.llm.scenario_prompts import get_course_prerequisites_prompt

st.set_page_config(page_title="Course Prerequisites", page_icon="📖", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} [data-testid="stSidebar"] {display: none;}
    .stApp { background: #f7f7f8; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif; }
    .stButton>button { background: white; color: #202123; border: 1px solid #d9d9e3; border-radius: 6px; padding: 0.75rem 1.5rem; width: 100%; }
</style>
""", unsafe_allow_html=True)

if st.button("← Back to Dashboard"):
    st.switch_page("pages/Student_Dashboard.py")

st.title("📖 Course Prerequisites")
st.caption("Understand what you need to know before taking a course and get preparation guidance")

with st.form("course_prerequisites_form"):
    st.markdown("### Target Course")
    
    course_name = st.text_input("Course You Want to Take", placeholder="e.g., Deep Learning, Advanced Algorithms")
    
    course_level = st.selectbox(
        "Course Level",
        ["Undergraduate", "Graduate", "Professional Certification", "Online Course"]
    )
    
    course_topics = st.text_area(
        "Course Topics (if known)",
        placeholder="List main topics covered in the course you want to take...",
        height=100
    )
    
    st.markdown("### Your Background")
    
    current_knowledge = st.text_area(
        "Your Current Knowledge",
        placeholder="List courses you've completed and topics you're familiar with...",
        height=120
    )
    
    learning_goal = st.text_input(
        "Why You Want to Take This Course",
        placeholder="e.g., Career change, academic requirement, personal interest..."
    )
    
    time_available = st.selectbox(
        "Time Available for Preparation",
        ["Already ready", "1-2 weeks", "1 month", "2-3 months", "3+ months"]
    )
    
    submitted = st.form_submit_button("Get Prerequisite Analysis", use_container_width=True)

if submitted and course_name and current_knowledge:
    prompt = get_course_prerequisites_prompt(
        course_name=course_name,
        course_level=course_level,
        course_topics=course_topics if course_topics else None,
        current_knowledge=current_knowledge,
        learning_goal=learning_goal if learning_goal else None,
        time_available=time_available
    )
    
    with st.spinner("Analyzing prerequisites and creating preparation plan..."):
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
            
            prerequisites = json.loads(json_str)
            st.session_state['prerequisites'] = prerequisites
            st.success("Prerequisite analysis complete!")
        except Exception as e:
            st.error(f"Analysis failed: {str(e)}")

if 'prerequisites' in st.session_state:
    prerequisites = st.session_state['prerequisites']
    
    st.markdown("---")
    st.markdown("## Prerequisite Analysis")
    
    # Readiness Assessment
    if 'readiness_assessment' in prerequisites:
        assessment = prerequisites['readiness_assessment']
        readiness = assessment.get('readiness_level', '')
        
        if readiness == "Ready":
            st.success(f"✅ **You are {readiness}** to take this course!")
        elif readiness == "Nearly Ready":
            st.info(f"🟡 **You are {readiness}** - just a bit more preparation needed")
        else:
            st.warning(f"⚠️ **Readiness Level: {readiness}** - preparation recommended")
        
        if assessment.get('explanation'):
            st.markdown(f"*{assessment['explanation']}*")
    
    # Required Prerequisites
    if 'required_prerequisites' in prerequisites:
        with st.expander("📚 Required Prerequisites", expanded=True):
            for prereq in prerequisites['required_prerequisites']:
                importance = prereq.get('importance', '')
                emoji = "🔴" if importance == "Critical" else "🟡" if importance == "Important" else "🟢"
                
                st.markdown(f"{emoji} **{prereq.get('topic', '')}**")
                st.markdown(f"**Why needed:** {prereq.get('why_needed', '')}")
                
                status = prereq.get('your_status', '')
                if status == "Strong":
                    st.success(f"Your status: {status} ✓")
                elif status == "Adequate":
                    st.info(f"Your status: {status}")
                else:
                    st.warning(f"Your status: {status} - needs work")
                
                st.markdown("---")
    
    # Preparation Plan
    if 'preparation_plan' in prerequisites:
        with st.expander("📋 Your Preparation Plan"):
            for phase in prerequisites['preparation_plan']:
                st.markdown(f"### {phase.get('phase', '')}")
                st.caption(f"Duration: {phase.get('duration', '')} | Priority: {phase.get('priority', '')}")
                
                if phase.get('topics_to_cover'):
                    st.markdown("**Topics to cover:**")
                    for topic in phase['topics_to_cover']:
                        st.markdown(f"  - {topic}")
                
                if phase.get('resources'):
                    st.markdown("**Resources:**")
                    for resource in phase['resources']:
                        st.markdown(f"  - {resource}")
                
                if phase.get('practice_activities'):
                    st.markdown("**Practice activities:**")
                    for activity in phase['practice_activities']:
                        st.markdown(f"  - {activity}")
                st.markdown("")
    
    # Knowledge Gaps
    if 'knowledge_gaps' in prerequisites:
        with st.expander("❌ Knowledge Gaps to Fill"):
            for gap in prerequisites['knowledge_gaps']:
                st.markdown(f"**{gap.get('gap', '')}**")
                st.caption(f"Impact: {gap.get('impact', '')} | Time to fill: {gap.get('time_to_fill', '')}")
                if gap.get('how_to_fill'):
                    st.markdown(f"*How to fill:* {gap['how_to_fill']}")
                st.markdown("")
    
    # Recommended Resources
    if 'recommended_resources' in prerequisites:
        with st.expander("📚 Recommended Resources"):
            for resource in prerequisites['recommended_resources']:
                st.markdown(f"**{resource.get('type', '')}:** {resource.get('title', '')}")
                st.caption(f"Focus: {resource.get('focus_area', '')} | Difficulty: {resource.get('difficulty', '')}")
                if resource.get('link'):
                    st.markdown(f"Link: {resource['link']}")
                st.markdown("")
    
    # Study Tips
    if 'study_tips' in prerequisites:
        with st.expander("💡 Study Tips"):
            for tip in prerequisites['study_tips']:
                st.info(f"• {tip}")
    
    st.markdown("---")
    st.download_button(
        label="Download Prerequisite Guide (JSON)",
        data=json.dumps(prerequisites, indent=2),
        file_name="course_prerequisites.json",
        mime="application/json",
        use_container_width=True
    )
