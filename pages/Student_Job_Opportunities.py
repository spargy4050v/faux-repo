"""
Job Opportunities - Student Tool
"""
import streamlit as st
import json
from src.llm.client import GeminiClient
from src.llm.scenario_prompts import get_job_opportunities_prompt

st.set_page_config(page_title="Job Opportunities", page_icon="💼", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} [data-testid="stSidebar"] {display: none;}
    .stApp { background: #f7f7f8; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif; }
    .stButton>button { background: white; color: #202123; border: 1px solid #d9d9e3; border-radius: 6px; padding: 0.75rem 1.5rem; width: 100%; }
</style>
""", unsafe_allow_html=True)

if st.button("← Back to Dashboard"):
    st.switch_page("pages/Student_Dashboard.py")

st.title("💼 Job Opportunities")
st.caption("Discover job roles, companies, and opportunities matching your skillset")

with st.form("job_opportunities_form"):
    st.markdown("### Your Background")
    
    col1, col2 = st.columns(2)
    with col1:
        education_level = st.selectbox(
            "Education Level",
            ["Undergraduate Student", "Bachelor's Degree", "Master's Student", "Master's Degree", "Ph.D"]
        )
    with col2:
        experience_years = st.selectbox("Years of Experience", ["0 (Fresher)", "1-2", "3-5", "5+"])
    
    field_of_study = st.text_input("Field of Study", placeholder="e.g., Computer Science, Data Science")
    
    skills = st.text_area(
        "Your Skills",
        placeholder="List your technical skills, programming languages, frameworks, tools...",
        height=100
    )
    
    st.markdown("### Preferences")
    
    job_types = st.multiselect(
        "Job Types of Interest",
        ["Full-time", "Internship", "Part-time", "Contract", "Remote", "Freelance"],
        default=["Full-time"]
    )
    
    preferred_industries = st.multiselect(
        "Preferred Industries",
        ["Technology/Software", "Finance", "Healthcare", "E-commerce", "Consulting", 
         "Manufacturing", "Education", "Gaming", "Startup", "Research"],
        default=["Technology/Software"]
    )
    
    location = st.text_input("Preferred Location (Optional)", placeholder="e.g., Bangalore, Remote, USA")
    
    interests = st.text_area(
        "Specific Interests (Optional)",
        placeholder="e.g., AI/ML, Backend Development, Cloud Computing...",
        height=60
    )
    
    submitted = st.form_submit_button("Find Job Opportunities", use_container_width=True)

if submitted and field_of_study and skills:
    prompt = get_job_opportunities_prompt(
        education_level=education_level,
        field_of_study=field_of_study,
        skills=skills,
        experience_years=experience_years,
        job_types=", ".join(job_types),
        preferred_industries=", ".join(preferred_industries),
        location=location if location else None,
        interests=interests if interests else None
    )
    
    with st.spinner("Finding matching job opportunities..."):
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
            
            opportunities = json.loads(json_str)
            st.session_state['job_opportunities'] = opportunities
            st.success("Job opportunities found!")
        except Exception as e:
            st.error(f"Search failed: {str(e)}")

if 'job_opportunities' in st.session_state:
    opportunities = st.session_state['job_opportunities']
    
    st.markdown("---")
    st.markdown("## Your Job Opportunities")
    
    if 'recommended_roles' in opportunities:
        with st.expander("🎯 Recommended Job Roles", expanded=True):
            for role in opportunities['recommended_roles']:
                match = role.get('match_percentage', 0)
                color = "🟢" if match >= 80 else "🟡" if match >= 60 else "🔵"
                st.markdown(f"{color} **{role.get('role_title', '')}** - {match}% match")
                st.markdown(f"**Description:** {role.get('description', '')}")
                st.caption(f"Typical Salary: {role.get('salary_range', '')} | Growth Potential: {role.get('growth_potential', '')}")
                
                if role.get('required_skills'):
                    st.markdown(f"**Key Skills:** {', '.join(role['required_skills'])}")
                if role.get('skill_gaps'):
                    st.warning(f"Skills to develop: {', '.join(role['skill_gaps'])}")
                st.markdown("---")
    
    if 'target_companies' in opportunities:
        with st.expander("🏢 Target Companies"):
            for company in opportunities['target_companies']:
                st.markdown(f"**{company.get('company_name', '')}**")
                st.markdown(f"Type: {company.get('company_type', '')} | Size: {company.get('size', '')}")
                st.caption(f"Why it's a fit: {company.get('why_good_fit', '')}")
                if company.get('typical_roles'):
                    st.markdown(f"Typical roles: {', '.join(company['typical_roles'])}")
                st.markdown("")
    
    if 'job_search_strategy' in opportunities:
        with st.expander("📋 Job Search Strategy"):
            for strategy in opportunities['job_search_strategy']:
                st.markdown(f"**{strategy.get('strategy', '')}**")
                st.markdown(f"{strategy.get('description', '')}")
                if strategy.get('action_items'):
                    st.markdown("Action items:")
                    for item in strategy['action_items']:
                        st.markdown(f"  - {item}")
                st.markdown("")
    
    if 'application_tips' in opportunities:
        with st.expander("💡 Application Tips"):
            for tip in opportunities['application_tips']:
                st.info(f"**{tip.get('area', '')}:** {tip.get('tip', '')}")
    
    if 'skill_development' in opportunities:
        with st.expander("📚 Skills to Develop"):
            for skill in opportunities['skill_development']:
                priority = skill.get('priority', '')
                emoji = "🔴" if priority == "High" else "🟡" if priority == "Medium" else "🟢"
                st.markdown(f"{emoji} **{skill.get('skill', '')}**")
                st.caption(f"Time to learn: {skill.get('time_to_learn', '')} | Resources: {skill.get('learning_resources', '')}")
    
    if 'networking_suggestions' in opportunities:
        with st.expander("🤝 Networking Suggestions"):
            for suggestion in opportunities['networking_suggestions']:
                st.markdown(f"- {suggestion}")
    
    st.markdown("---")
    st.download_button(
        label="Download Job Opportunities (JSON)",
        data=json.dumps(opportunities, indent=2),
        file_name="job_opportunities.json",
        mime="application/json",
        use_container_width=True
    )
