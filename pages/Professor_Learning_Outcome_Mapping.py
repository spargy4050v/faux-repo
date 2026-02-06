"""
Learning Outcome Mapping - Professor Tool
"""
import streamlit as st
import json
from src.llm.client import GeminiClient
from src.llm.scenario_prompts import get_learning_outcome_mapping_prompt

st.set_page_config(page_title="Learning Outcome Mapping", page_icon="🎯", layout="centered", initial_sidebar_state="collapsed")

# CSS
st.markdown("""
<style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} [data-testid="stSidebar"] {display: none;}
    .stApp { background: #f7f7f8; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif; }
    .stButton>button { background: white; color: #202123; border: 1px solid #d9d9e3; border-radius: 6px; padding: 0.75rem 1.5rem; width: 100%; }
</style>
""", unsafe_allow_html=True)

if st.button("← Back to Dashboard"):
    st.switch_page("pages/Professor_Dashboard.py")

st.title("🎯 Learning Outcome Mapping")
st.caption("Map course topics to program outcomes and accreditation standards")

# Form
with st.form("outcome_mapping_form"):
    st.markdown("### Course Information")
    
    course_name = st.text_input("Course Name", placeholder="e.g., Database Management Systems")
    
    program_type = st.selectbox(
        "Program Type",
        ["B.Tech", "M.Tech", "MBA", "MCA", "Ph.D", "Other"]
    )
    
    col1, col2 = st.columns(2)
    with col1:
        course_level = st.selectbox("Course Level", ["Introductory", "Intermediate", "Advanced", "Graduate"])
    with col2:
        credit_hours = st.number_input("Credit Hours", min_value=1, max_value=6, value=3)
    
    st.markdown("### Course Content")
    
    topics_covered = st.text_area(
        "Major Topics Covered",
        placeholder="List the main topics and units covered in this course...",
        height=150
    )
    
    existing_outcomes = st.text_area(
        "Current Learning Outcomes (Optional)",
        placeholder="If you have existing learning outcomes, paste them here for refinement...",
        height=100
    )
    
    st.markdown("### Accreditation Framework")
    
    framework = st.multiselect(
        "Target Frameworks",
        ["NBA (India)", "ABET", "Bloom's Taxonomy", "ACM/IEEE CS Curricula", "Custom"],
        default=["Bloom's Taxonomy"]
    )
    
    submitted = st.form_submit_button("Generate Outcome Mapping", use_container_width=True)

if submitted and course_name and topics_covered:
    prompt = get_learning_outcome_mapping_prompt(
        course_name=course_name,
        program_type=program_type,
        course_level=course_level,
        credit_hours=credit_hours,
        topics_covered=topics_covered,
        accreditation_framework=", ".join(framework),
        existing_outcomes=existing_outcomes if existing_outcomes else None
    )
    
    with st.spinner("Mapping learning outcomes to topics and standards..."):
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
            
            mapping = json.loads(json_str)
            st.session_state['outcome_mapping'] = mapping
            st.success("Learning outcome mapping generated!")
        except Exception as e:
            st.error(f"Generation failed: {str(e)}")

# Display Results
if 'outcome_mapping' in st.session_state:
    mapping = st.session_state['outcome_mapping']
    
    st.markdown("---")
    st.markdown("## Learning Outcome Mapping")
    
    # Course Learning Outcomes
    if 'learning_outcomes' in mapping:
        with st.expander("📋 Course Learning Outcomes (CLOs)", expanded=True):
            for outcome in mapping['learning_outcomes']:
                st.markdown(f"**CLO-{outcome.get('clo_number', '')}:** {outcome.get('outcome_statement', '')}")
                st.caption(f"Bloom's Level: {outcome.get('blooms_level', '')} | Assessment: {outcome.get('assessment_method', '')}")
                st.markdown("")
    
    # Topic Mapping
    if 'topic_outcome_mapping' in mapping:
        with st.expander("🔗 Topic-to-Outcome Mapping"):
            for item in mapping['topic_outcome_mapping']:
                st.markdown(f"**Topic:** {item.get('topic', '')}")
                st.markdown(f"Mapped to: {', '.join([f'CLO-{clo}' for clo in item.get('clos', [])])}")
                if item.get('teaching_strategies'):
                    st.caption(f"Teaching Strategies: {', '.join(item['teaching_strategies'])}")
                st.markdown("---")
    
    # Program Outcome Mapping
    if 'program_outcome_mapping' in mapping:
        with st.expander("🎓 Program Outcome (PO) Mapping"):
            for po in mapping['program_outcome_mapping']:
                st.markdown(f"**{po.get('po_code', '')}:** {po.get('po_description', '')}")
                st.caption(f"Mapped CLOs: {', '.join([f'CLO-{clo}' for clo in po.get('mapped_clos', [])])} | Strength: {po.get('mapping_strength', '')}")
    
    # Assessment Strategy
    if 'assessment_strategy' in mapping:
        with st.expander("📝 Assessment Strategy"):
            for assessment in mapping['assessment_strategy']:
                st.markdown(f"**{assessment.get('assessment_type', '')}** ({assessment.get('weightage', '')}%)")
                st.markdown(f"Evaluates: {', '.join([f'CLO-{clo}' for clo in assessment.get('evaluates_clos', [])])}")
                st.caption(f"Description: {assessment.get('description', '')}")
                st.markdown("")
    
    # Accreditation Alignment
    if 'accreditation_alignment' in mapping:
        with st.expander("✅ Accreditation Alignment"):
            for align in mapping['accreditation_alignment']:
                st.markdown(f"**{align.get('framework', '')}**")
                st.markdown(f"Standards Met: {', '.join(align.get('standards_met', []))}")
                if align.get('gaps'):
                    st.warning(f"Gaps: {', '.join(align['gaps'])}")
    
    # Download
    st.markdown("---")
    st.download_button(
        label="Download Outcome Mapping (JSON)",
        data=json.dumps(mapping, indent=2),
        file_name=f"{course_name.replace(' ', '_')}_outcome_mapping.json",
        mime="application/json",
        use_container_width=True
    )
