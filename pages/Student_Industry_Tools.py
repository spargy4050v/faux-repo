"""
Industry Tools & Tech - Student Tool
"""
import streamlit as st
import json
from src.llm.client import GeminiClient
from src.llm.scenario_prompts import get_industry_tools_prompt

st.set_page_config(page_title="Industry Tools & Tech", page_icon="🛠️", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} [data-testid="stSidebar"] {display: none;}
    .stApp { background: #f7f7f8; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif; }
    .stButton>button { background: white; color: #202123; border: 1px solid #d9d9e3; border-radius: 6px; padding: 0.75rem 1.5rem; width: 100%; }
</style>
""", unsafe_allow_html=True)

if st.button("← Back to Dashboard"):
    st.switch_page("pages/Student_Dashboard.py")

st.title("🛠️ Industry Tools & Technologies")
st.caption("Discover the tools and technologies used in your target industry or role")

with st.form("industry_tools_form"):
    st.markdown("### Target Role/Industry")
    
    target_role = st.text_input("Target Job Role", placeholder="e.g., Data Scientist, Full Stack Developer")
    
    industry = st.multiselect(
        "Industry",
        ["Technology/Software", "Finance/Banking", "Healthcare", "E-commerce", 
         "Consulting", "Manufacturing", "Education", "Gaming", "Startups", "Research"],
        default=["Technology/Software"]
    )
    
    company_size = st.selectbox(
        "Preferred Company Size",
        ["Startup (1-50)", "Small (51-200)", "Medium (201-1000)", "Large (1000+)", "Any"]
    )
    
    st.markdown("### Your Current State")
    
    current_tools = st.text_area(
        "Tools/Technologies You Currently Know",
        placeholder="List tools, frameworks, languages, platforms you're familiar with...",
        height=100
    )
    
    experience_level = st.selectbox(
        "Your Experience Level",
        ["Student", "Entry Level (0-2 years)", "Mid Level (3-5 years)", "Senior (5+ years)"]
    )
    
    st.markdown("### Learning Preferences")
    
    focus_area = st.multiselect(
        "Focus Areas",
        ["Programming Languages", "Frameworks/Libraries", "Cloud Platforms", 
         "DevOps Tools", "Databases", "Development Tools", "AI/ML Tools", 
         "Security Tools", "Collaboration Tools"],
        default=["Programming Languages", "Frameworks/Libraries"]
    )
    
    urgency = st.selectbox(
        "Learning Timeline",
        ["Immediate (job search)", "3 months", "6 months", "1 year", "Just exploring"]
    )
    
    submitted = st.form_submit_button("Get Tool Recommendations", use_container_width=True)

if submitted and target_role:
    prompt = get_industry_tools_prompt(
        target_role=target_role,
        industry=", ".join(industry),
        company_size=company_size,
        current_tools=current_tools if current_tools else "Beginner",
        experience_level=experience_level,
        focus_areas=", ".join(focus_area),
        timeline=urgency
    )
    
    with st.spinner("Analyzing industry tools and technologies..."):
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
            
            tools_data = json.loads(json_str)
            st.session_state['industry_tools'] = tools_data
            st.success("Tool recommendations generated!")
        except Exception as e:
            st.error(f"Analysis failed: {str(e)}")

if 'industry_tools' in st.session_state:
    tools_data = st.session_state['industry_tools']
    
    st.markdown("---")
    st.markdown("## Industry Tools & Technologies")
    
    # Essential Tools
    if 'essential_tools' in tools_data:
        with st.expander("🔥 Must-Learn Tools", expanded=True):
            for tool in tools_data['essential_tools']:
                importance = tool.get('importance', '')
                emoji = "🔴" if importance == "Critical" else "🟡" if importance == "High" else "🟢"
                
                st.markdown(f"{emoji} **{tool.get('tool_name', '')}**")
                st.markdown(f"Category: {tool.get('category', '')} | Importance: {importance}")
                st.markdown(f"**Use case:** {tool.get('use_case', '')}")
                st.caption(f"Learning curve: {tool.get('learning_curve', '')} | Market demand: {tool.get('market_demand', '')}")
                
                if tool.get('why_essential'):
                    st.info(f"Why learn: {tool['why_essential']}")
                st.markdown("---")
    
    # Optional/Nice-to-Have Tools
    if 'optional_tools' in tools_data:
        with st.expander("➕ Nice-to-Have Tools"):
            for tool in tools_data['optional_tools']:
                st.markdown(f"**{tool.get('tool_name', '')}**")
                st.caption(f"Category: {tool.get('category', '')} | Advantage: {tool.get('advantage', '')}")
                st.markdown("")
    
    # Learning Path
    if 'learning_path' in tools_data:
        with st.expander("📚 Recommended Learning Path"):
            for step in tools_data['learning_path']:
                st.markdown(f"### Step {step.get('step', '')}: {step.get('phase', '')}")
                st.caption(f"Duration: {step.get('duration', '')}")
                
                if step.get('tools_to_learn'):
                    st.markdown("**Tools to learn:**")
                    for tool in step['tools_to_learn']:
                        st.markdown(f"  - {tool}")
                
                if step.get('learning_resources'):
                    st.markdown("**Resources:**")
                    for resource in step['learning_resources']:
                        st.markdown(f"  - {resource}")
                
                if step.get('projects'):
                    st.markdown("**Practice projects:**")
                    for project in step['projects']:
                        st.markdown(f"  - {project}")
                st.markdown("")
    
    # Toolstack Examples
    if 'typical_toolstacks' in tools_data:
        with st.expander("🏗️ Typical Tool Stacks"):
            for stack in tools_data['typical_toolstacks']:
                st.markdown(f"**{stack.get('stack_name', '')}**")
                st.markdown(f"Used for: {stack.get('use_case', '')}")
                if stack.get('tools'):
                    st.markdown(f"Tools: {', '.join(stack['tools'])}")
                st.caption(f"Popularity: {stack.get('popularity', '')}")
                st.markdown("")
    
    # Emerging Technologies
    if 'emerging_technologies' in tools_data:
        with st.expander("🚀 Emerging Technologies to Watch"):
            for tech in tools_data['emerging_technologies']:
                st.markdown(f"**{tech.get('technology', '')}**")
                st.markdown(f"Status: {tech.get('adoption_status', '')} | Future potential: {tech.get('future_potential', '')}")
                st.caption(f"Recommendation: {tech.get('recommendation', '')}")
                st.markdown("")
    
    # Certifications
    if 'relevant_certifications' in tools_data:
        with st.expander("🎓 Relevant Certifications"):
            for cert in tools_data['relevant_certifications']:
                st.markdown(f"**{cert.get('certification', '')}**")
                st.markdown(f"Provider: {cert.get('provider', '')}")
                st.caption(f"Value: {cert.get('value', '')} | Cost: {cert.get('cost', '')} | Time: {cert.get('time_required', '')}")
                st.markdown("")
    
    # Practical Tips
    if 'practical_tips' in tools_data:
        with st.expander("💡 Practical Learning Tips"):
            for tip in tools_data['practical_tips']:
                st.info(f"• {tip}")
    
    st.markdown("---")
    st.download_button(
        label="Download Tools Guide (JSON)",
        data=json.dumps(tools_data, indent=2),
        file_name="industry_tools_guide.json",
        mime="application/json",
        use_container_width=True
    )
