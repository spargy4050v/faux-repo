"""
GenAI Curriculum Generator - Streamlit Application
RAG-powered curriculum generation using ChromaDB + Google Gemini (Free Tier)
"""
import streamlit as st
import os
from src.rag.vector_store import CurriculumVectorStore
from src.llm.client import GeminiClient
from src.curriculum.generator import CurriculumGenerator
from src.curriculum.validator import CurriculumValidator
from src.curriculum.models import CurriculumRequest
from src.pdf.generator import CurriculumPDFGenerator


# Page configuration
st.set_page_config(
    page_title="GenAI Curriculum Generator",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #2C3E50;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #7F8C8D;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        font-size: 1.1rem;
        padding: 0.75rem;
        border-radius: 8px;
    }
    .info-box {
        background-color: #E8F5E9;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #4CAF50;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def initialize_components():
    """Initialize vector store, LLM client, and generator (cached)."""
    try:
        # Check if knowledge base exists
        if not os.path.exists("./data/vector_db"):
            st.error("""
            ⚠️ **Knowledge base not initialized!**
            
            Please run the following command first:
            ```
            python populate_knowledge_base.py
            ```
            """)
            st.stop()
        
        vector_store = CurriculumVectorStore()
        
        if vector_store.get_count() == 0:
            st.error("""
            ⚠️ **Knowledge base is empty!**
            
            Please run the following command to populate it:
            ```
            python populate_knowledge_base.py
            ```
            """)
            st.stop()
        
        llm_client = GeminiClient()
        generator = CurriculumGenerator(vector_store, llm_client)
        validator = CurriculumValidator()
        pdf_generator = CurriculumPDFGenerator()
        
        return generator, validator, pdf_generator, vector_store
    
    except ValueError as e:
        st.error(f"""
        ⚠️ **Configuration Error:** {str(e)}
        
        Please create a `.env` file with your Google API key:
        ```
        GOOGLE_API_KEY=your_api_key_here
        ```
        
        Get your free API key from: https://makersuite.google.com/app/apikey
        """)
        st.stop()
    except Exception as e:
        st.error(f"❌ Initialization failed: {str(e)}")
        st.stop()


def main():
    """Main Streamlit application."""
    
    # Header
    st.markdown('<div class="main-header">🎓 GenAI Curriculum Generator</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-header">AI-Powered Educational Curriculum Design with RAG</div>',
        unsafe_allow_html=True
    )
    
    # Initialize components
    generator, validator, pdf_generator, vector_store = initialize_components()
    
    # Sidebar - Configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        st.markdown(f"""
        <div class="info-box">
        <b>🗄️ Knowledge Base</b><br/>
        Documents: {vector_store.get_count()}<br/>
        Status: ✅ Ready
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        use_rag = st.checkbox("Use RAG Context", value=True, help="Retrieve similar curricula for better generation")
        
        st.markdown("---")
        
        st.markdown("""
        ### 💡 About
        This app uses:
        - **Google Gemini 1.5 Pro** (Free)
        - **ChromaDB** (Local Vector Store)
        - **RAG** for context-aware generation
        
        **Free Tier Limits:**
        - 60 requests/min
        - 1500 requests/day
        """)
    
    # Main content
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📝 Curriculum Parameters")
        
        # Input form
        with st.form("curriculum_form"):
            skill = st.text_input(
                "Subject/Skill Area *",
                placeholder="e.g., Machine Learning, Data Science, Web Development",
                help="The main subject or skill area for the curriculum"
            )
            
            level = st.selectbox(
                "Education Level *",
                options=["BTech", "Masters", "Diploma", "Certification"],
                help="The academic level of the curriculum"
            )
            
            duration = st.number_input(
                "Duration (Semesters) *",
                min_value=1,
                max_value=12,
                value=4,
                help="Number of semesters/modules"
            )
            
            specialization = st.text_input(
                "Specialization (Optional)",
                placeholder="e.g., Deep Learning, Cloud Computing",
                help="Specific area of focus within the subject"
            )
            
            focus_areas = st.text_area(
                "Focus Areas (Optional)",
                placeholder="Enter focus areas, one per line",
                help="Specific topics or skills to emphasize"
            )
            
            submitted = st.form_submit_button("🚀 Generate Curriculum")
        
        if submitted:
            if not skill:
                st.error("⚠️ Please enter a subject/skill area")
            else:
                # Parse focus areas
                focus_list = None
                if focus_areas:
                    focus_list = [area.strip() for area in focus_areas.split('\n') if area.strip()]
                
                # Create request
                request = CurriculumRequest(
                    skill=skill,
                    level=level,
                    duration_semesters=duration,
                    specialization=specialization if specialization else None,
                    focus_areas=focus_list
                )
                
                # Store in session state and trigger generation
                st.session_state['request'] = request
                st.session_state['use_rag'] = use_rag
                st.session_state['generate_new'] = True  # Flag to trigger generation
    
    with col2:
        st.header("📊 Generated Curriculum")
        
        # Only generate if explicitly requested
        if st.session_state.get('generate_new', False):
            request = st.session_state['request']
            use_rag = st.session_state.get('use_rag', True)
            
            # Generate curriculum
            with st.spinner("🤖 Generating curriculum... This may take 30-60 seconds..."):
                try:
                    curriculum = generator.generate(request, use_rag=use_rag)
                    st.session_state['curriculum'] = curriculum
                    
                    # Validate
                    validation_report = validator.validate_and_report(curriculum)
                    st.session_state['validation'] = validation_report
                    
                    # Clear the generation flag
                    st.session_state['generate_new'] = False
                    
                    st.success("✅ Curriculum generated successfully!")
                
                except Exception as e:
                    st.error(f"❌ Generation failed: {str(e)}")
                    st.session_state['generate_new'] = False
                    st.stop()
        
        if 'curriculum' in st.session_state:
            curriculum = st.session_state['curriculum']
            
            # Display curriculum
            st.subheader(curriculum.title)
            
            st.markdown(f"""
            **Level:** {curriculum.level}  
            **Duration:** {curriculum.duration_semesters} Semesters  
            **Total Credits:** {curriculum.total_credits}
            """)
            
            # Tabs for different sections
            tab1, tab2, tab3, tab4 = st.tabs(["📖 Overview", "📚 Semesters", "🎯 Outcomes", "✅ Validation"])
            
            with tab1:
                st.markdown("### Overview")
                st.write(curriculum.overview)
                
                if curriculum.career_paths:
                    st.markdown("### Career Paths")
                    for career in curriculum.career_paths:
                        st.markdown(f"- {career}")
            
            with tab2:
                st.markdown("### Semester-wise Breakdown")
                for semester in curriculum.semesters:
                    with st.expander(f"Semester {semester.semester_number} ({semester.total_credits} Credits)"):
                        for course in semester.courses:
                            st.markdown(f"""
                            **{course.code} - {course.name}** ({course.credits} credits)  
                            *{course.category}*  
                            {course.description}
                            """)
                            if course.prerequisites:
                                st.caption(f"Prerequisites: {', '.join(course.prerequisites)}")
                            st.markdown("---")
            
            with tab3:
                st.markdown("### Learning Outcomes")
                for outcome in curriculum.learning_outcomes:
                    st.markdown(f"✓ {outcome}")
            
            with tab4:
                validation = st.session_state.get('validation', '')
                if "✓" in validation:
                    st.success(validation)
                else:
                    st.warning(validation)
            
            # Download PDF button
            st.markdown("---")
            try:
                pdf_buffer = pdf_generator.generate(curriculum)
                
                st.download_button(
                    label="📥 Download Curriculum PDF",
                    data=pdf_buffer,
                    file_name=f"{curriculum.title.replace(' ', '_')}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            
            except Exception as e:
                st.error(f"❌ PDF generation failed: {str(e)}")
        else:
            st.info("👈 Fill in the parameters and click 'Generate Curriculum' to get started!")


if __name__ == "__main__":
    main()
