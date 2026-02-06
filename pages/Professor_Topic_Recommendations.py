"""
Topic Recommendations - Professor Tool
"""
import streamlit as st
import json
from src.llm.client import GeminiClient
from src.llm.scenario_prompts import get_topic_recommendations_prompt

st.set_page_config(page_title="Topic Recommendations", page_icon="📚", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} [data-testid="stSidebar"] {display: none;}
    .stApp { background: #f7f7f8; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif; }
    .stButton>button { background: white; color: #202123; border: 1px solid #d9d9e3; border-radius: 6px; padding: 0.75rem 1.5rem; width: 100%; }
</style>
""", unsafe_allow_html=True)

if st.button("← Back to Dashboard"):
    st.switch_page("pages/Professor_Dashboard.py")

st.title("📚 Topic Recommendations")
st.caption("Get suggestions for topics to add, update, or remove in your courses")

with st.form("topic_recommendations_form"):
    st.markdown("### Course Information")
    
    course_name = st.text_input("Course Name", placeholder="e.g., Advanced Machine Learning")
    
    col1, col2 = st.columns(2)
    with col1:
        course_level = st.selectbox("Course Level", ["Undergraduate", "Graduate", "Professional"])
    with col2:
        course_duration = st.selectbox("Course Duration", ["4 weeks", "8 weeks", "12 weeks", "16 weeks", "1 semester", "2 semesters"])
    
    current_topics = st.text_area(
        "Current Topics Covered",
        placeholder="List topics currently taught in this course...",
        height=150
    )
    
    st.markdown("### Context")
    
    field = st.selectbox(
        "Field/Domain",
        ["Artificial Intelligence", "Data Science", "Software Engineering", "Computer Networks",
         "Web Development", "Mobile Development", "Cloud Computing", "Cybersecurity", 
         "Database Systems", "Other"]
    )
    
    student_background = st.text_input(
        "Student Background",
        placeholder="e.g., Completed courses in programming, statistics..."
    )
    
    update_goals = st.multiselect(
        "Update Goals",
        ["Add emerging technologies", "Remove outdated content", "Improve depth", 
         "Add practical applications", "Align with industry trends", "Balance theory and practice"],
        default=["Add emerging technologies"]
    )
    
    submitted = st.form_submit_button("Get Topic Recommendations", use_container_width=True)

if submitted and course_name and current_topics:
    prompt = get_topic_recommendations_prompt(
        course_name=course_name,
        course_level=course_level,
        current_topics=current_topics,
        field=field,
        student_background=student_background if student_background else None,
        update_goals=", ".join(update_goals)
    )
    
    with st.spinner("Generating topic recommendations..."):
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
            
            recommendations = json.loads(json_str)
            st.session_state['topic_recommendations'] = recommendations
            st.success("Topic recommendations generated!")
        except Exception as e:
            st.error(f"Recommendation generation failed: {str(e)}")

if 'topic_recommendations' in st.session_state:
    recommendations = st.session_state['topic_recommendations']
    
    st.markdown("---")
    st.markdown("## Topic Recommendations")
    
    if 'topics_to_add' in recommendations:
        with st.expander("➕ Topics to Add", expanded=True):
            for topic in recommendations['topics_to_add']:
                st.markdown(f"### {topic.get('topic', '')}")
                st.markdown(f"**Rationale:** {topic.get('rationale', '')}")
                st.caption(f"Priority: {topic.get('priority', '')} | Suggested Duration: {topic.get('suggested_duration', '')}")
                if topic.get('learning_outcomes'):
                    st.markdown("**Learning Outcomes:**")
                    for outcome in topic['learning_outcomes']:
                        st.markdown(f"  - {outcome}")
                if topic.get('teaching_resources'):
                    st.markdown("**Resources:**")
                    for resource in topic['teaching_resources']:
                        st.markdown(f"  - {resource}")
                st.markdown("---")
    
    if 'topics_to_update' in recommendations:
        with st.expander("🔄 Topics to Update"):
            for topic in recommendations['topics_to_update']:
                st.markdown(f"**{topic.get('topic', '')}**")
                st.markdown(f"Current Status: {topic.get('current_status', '')}")
                st.markdown(f"**Suggested Update:** {topic.get('suggested_update', '')}")
                st.caption(f"Reason: {topic.get('reason', '')}")
                st.markdown("")
    
    if 'topics_to_remove' in recommendations:
        with st.expander("➖ Topics to Consider Removing"):
            for topic in recommendations['topics_to_remove']:
                st.markdown(f"**{topic.get('topic', '')}**")
                st.markdown(f"**Reason:** {topic.get('reason', '')}")
                if topic.get('alternative'):
                    st.info(f"Alternative: {topic['alternative']}")
                st.markdown("")
    
    if 'topic_sequence' in recommendations:
        with st.expander("📋 Suggested Topic Sequence"):
            for idx, item in enumerate(recommendations['topic_sequence'], 1):
                st.markdown(f"{idx}. **{item.get('topic', '')}** ({item.get('duration', '')})")
                st.caption(f"Builds on: {item.get('builds_on', 'Fundamentals')}")
    
    if 'emerging_trends' in recommendations:
        with st.expander("🚀 Emerging Trends in This Field"):
            for trend in recommendations['emerging_trends']:
                st.markdown(f"**{trend.get('trend', '')}**")
                st.markdown(f"Relevance: {trend.get('relevance', '')} | Maturity: {trend.get('maturity_level', '')}")
                st.caption(f"Recommendation: {trend.get('recommendation', '')}")
                st.markdown("")
    
    st.markdown("---")
    st.download_button(
        label="Download Topic Recommendations (JSON)",
        data=json.dumps(recommendations, indent=2),
        file_name="topic_recommendations.json",
        mime="application/json",
        use_container_width=True
    )
