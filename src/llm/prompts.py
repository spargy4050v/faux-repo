"""
Curriculum generation prompts for Gemini.
"""


def get_system_prompt() -> str:
    """Get system prompt for curriculum generation."""
    return """You are an expert curriculum designer with deep knowledge of educational standards, 
learning pathways, and industry requirements. You create comprehensive, well-structured curricula 
for various educational levels (BTech, Masters, Diplomas, Certifications) across different subjects.

Your curricula are:
- Pedagogically sound with proper prerequisite chains
- Industry-relevant with practical components
- Balanced in terms of theory, labs, and projects
- Aligned with credit hour standards
- Progressive in difficulty across semesters"""


def get_curriculum_generation_prompt(
    skill: str,
    level: str,
    duration_semesters: int,
    specialization: str = None,
    focus_areas: list = None,
    context: str = ""
) -> str:
    """
    Generate curriculum creation prompt.
    
    Args:
        skill: Subject/skill area
        level: Education level
        duration_semesters: Number of semesters
        specialization: Optional specialization
        focus_areas: Optional focus areas
        context: RAG context with similar curricula
        
    Returns:
        Complete prompt for Gemini
    """
    prompt_parts = [get_system_prompt()]
    
    # Add RAG context if available
    if context:
        prompt_parts.append(f"\n{context}\n")
    
    # Main instruction
    prompt_parts.append(f"""
Create a comprehensive {level} curriculum for {skill} spanning {duration_semesters} semesters.
""")
    
    if specialization:
        prompt_parts.append(f"Specialization: {specialization}")
    
    if focus_areas:
        prompt_parts.append(f"Focus Areas: {', '.join(focus_areas)}")
    
    # Output format instructions
    prompt_parts.append("""
Provide the curriculum in the following JSON format:

{
  "title": "Full curriculum title",
  "level": "Education level",
  "duration_semesters": number,
  "total_credits": number,
  "overview": "Brief overview of the curriculum",
  "learning_outcomes": ["outcome 1", "outcome 2", ...],
  "career_paths": ["career 1", "career 2", ...],
  "semesters": [
    {
      "semester_number": 1,
      "total_credits": number,
      "courses": [
        {
          "code": "COURSE101",
          "name": "Course Name",
          "credits": 3,
          "description": "Course description",
          "prerequisites": ["PREREQ101"],
          "category": "Core/Elective/Lab"
        }
      ]
    }
  ]
}

Guidelines:
1. Each course must have between 1-6 credits (typically 3-4 for theory, 1-2 for labs)
2. Each semester should have 15-20 total credits
3. Include a mix of Core, Elective, and Lab courses
4. Ensure proper prerequisite chains
5. Progress from foundational to advanced topics
6. Include practical/project courses
7. Make course codes realistic (e.g., CS101, ML201)
8. Provide detailed course descriptions

Return ONLY the JSON object, no additional text.
""")
    
    return "\n".join(prompt_parts)


def get_validation_prompt(curriculum_json: str) -> str:
    """
    Generate validation prompt for curriculum quality check.
    
    Args:
        curriculum_json: Generated curriculum in JSON format
        
    Returns:
        Validation prompt
    """
    return f"""Review this curriculum and identify any issues:

{curriculum_json}

Check for:
1. Prerequisite chain validity
2. Credit hour balance across semesters
3. Logical progression of topics
4. Missing essential courses
5. Unrealistic course loads

Provide a brief assessment and suggest improvements if needed.
"""
