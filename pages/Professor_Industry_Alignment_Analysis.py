"""
Industry Alignment Analysis - Professor Tool
"""
import streamlit as st
import json
from src.llm.client import GeminiClient
from src.llm.scenario_prompts import get_industry_alignment_prompt

st.set_page_config(page_title="Industry Alignment Analysis", page_icon="🏭", layout="centered", initial_sidebar_state="collapsed")

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

st.title("🏭 Industry Alignment Analysis")
st.caption("Analyze how well your curriculum aligns with current industry demands")

# Form
with st.form("industry_alignment_form"):
    st.markdown("### Program Details")
    
    program_name = st.text_input("Program Name", placeholder="e.g., B.Tech in Computer Science")
    
    col1, col2 = st.columns(2)
    with col1:
        specialization = st.text_input("Specialization/Track", placeholder="e.g., AI & ML, Data Science")
    with col2:
        program_duration = st.selectbox("Program Duration", ["2 Years", "3 Years", "4 Years", "5 Years"])
    
    st.markdown("### Current Curriculum")
    
    core_courses = st.text_area(
        "Core Courses Offered",
        placeholder="List the main courses in your program...",
        height=120
    )
    
    elective_courses = st.text_area(
        "Elective Courses (Optional)",
        placeholder="List elective courses offered...",
        height=80
    )
    
    st.markdown("### Industry Context")
    
    target_industries = st.multiselect(
        "Target Industries for Graduates",
        ["Software/IT Services", "Product Companies", "Consulting", "Finance/Banking", 
         "Healthcare Tech", "Manufacturing", "Research", "Startups", "Government/PSU"],
        default=["Software/IT Services"]
    )
    
    geographic_region = st.selectbox(
        "Primary Geographic Region",
        ["India", "USA", "Europe", "Asia-Pacific", "Global"]
    )
    
    submitted = st.form_submit_button("Analyze Industry Alignment", use_container_width=True)

if submitted and program_name and core_courses:
    prompt = get_industry_alignment_prompt(
        program_name=program_name,
        specialization=specialization if specialization else "General",
        core_courses=core_courses,
        elective_courses=elective_courses if elective_courses else None,
        target_industries=", ".join(target_industries),
        geographic_region=geographic_region
    )
    
    with st.spinner("Analyzing industry alignment..."):
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
            
            analysis = json.loads(json_str)
            st.session_state['industry_analysis'] = analysis
            st.success("Industry alignment analysis complete!")
        except Exception as e:
            st.error(f"Analysis failed: {str(e)}")

# Display Results
if 'industry_analysis' in st.session_state:
    analysis = st.session_state['industry_analysis']
    
    st.markdown("---")
    st.markdown("## Industry Alignment Report")
    
    # Alignment Score
    if 'overall_alignment_score' in analysis:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Overall Alignment", f"{analysis.get('overall_alignment_score', 0)}%")
        with col2:
            st.metric("Technical Skills", f"{analysis.get('technical_alignment', 0)}%")
        with col3:
            st.metric("Industry Tools", f"{analysis.get('tools_alignment', 0)}%")
    
    # Industry Skill Demands
    if 'industry_skill_demands' in analysis:
        with st.expander("📊 Current Industry Skill Demands", expanded=True):
            for skill in analysis['industry_skill_demands']:
                demand = skill.get('demand_level', '')
                emoji = "🔥" if demand == "Very High" else "⬆️" if demand == "High" else "➡️"
                st.markdown(f"{emoji} **{skill.get('skill', '')}** - Demand: {demand}")
                st.caption(f"Trend: {skill.get('trend', '')} | Salary Impact: {skill.get('salary_impact', '')}")
    
    # Coverage Analysis
    if 'curriculum_coverage' in analysis:
        with st.expander("✅ Curriculum Coverage Analysis"):
            for item in analysis['curriculum_coverage']:
                coverage = item.get('coverage_status', '')
                icon = "✅" if coverage == "Well Covered" else "⚠️" if coverage == "Partially Covered" else "❌"
                st.markdown(f"{icon} **{item.get('skill_area', '')}**")
                st.markdown(f"Status: {coverage}")
                if item.get('courses_covering'):
                    st.caption(f"Covered in: {', '.join(item['courses_covering'])}")
                if item.get('gaps'):
                    st.warning(f"Gaps: {item['gaps']}")
                st.markdown("")
    
    # Missing Skills
    if 'missing_critical_skills' in analysis:
        with st.expander("🚨 Missing Critical Skills"):
            for skill in analysis['missing_critical_skills']:
                st.markdown(f"**{skill.get('skill', '')}**")
                st.markdown(f"Industry Importance: {skill.get('importance', '')}")
                st.caption(f"Recommendation: {skill.get('recommendation', '')}")
                st.markdown("---")
    
    # Emerging Technologies
    if 'emerging_technologies' in analysis:
        with st.expander("🚀 Emerging Technologies to Consider"):
            for tech in analysis['emerging_technologies']:
                st.markdown(f"**{tech.get('technology', '')}**")
                st.markdown(f"Adoption Stage: {tech.get('adoption_stage', '')} | Relevance: {tech.get('relevance', '')}")
                st.caption(f"Suggested Action: {tech.get('suggested_action', '')}")
                st.markdown("")
    
    # Recommendations
    if 'recommendations' in analysis:
        with st.expander("💡 Actionable Recommendations"):
            for rec in analysis['recommendations']:
                priority = rec.get('priority', '')
                emoji = "🔴" if priority == "High" else "🟡" if priority == "Medium" else "🟢"
                st.markdown(f"{emoji} **{rec.get('recommendation', '')}**")
                st.caption(f"Priority: {priority} | Implementation Effort: {rec.get('implementation_effort', '')}")
                if rec.get('expected_impact'):
                    st.success(f"Expected Impact: {rec['expected_impact']}")
                st.markdown("")
    
    # Download
    st.markdown("---")
    st.download_button(
        label="Download Industry Analysis (JSON)",
        data=json.dumps(analysis, indent=2),
        file_name=f"{program_name.replace(' ', '_')}_industry_analysis.json",
        mime="application/json",
        use_container_width=True
    )
