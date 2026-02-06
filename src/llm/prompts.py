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
IMPORTANT: You must return ONLY a valid JSON object. No markdown, no explanations, just pure JSON.

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

JSON FORMATTING RULES:
⚠️ Use double quotes for all strings, not single quotes
⚠️ Escape any quotes within strings with backslash: \"
⚠️ No trailing commas after last items in arrays or objects
⚠️ All strings must be properly closed
⚠️ Course descriptions should be single sentences without line breaks

CRITICAL REQUIREMENT - COURSE CREDITS:
⚠️ EVERY course "credits" field MUST be a number between 1 and 6 (inclusive).
- Theory courses: Use 3 or 4 credits
- Lab courses: Use 1 or 2 credits  
- Project courses: Use 2 or 3 credits
- NEVER use 7, 8, 9, 10, or higher credits for any single course
- To reach semester credit totals, use multiple courses instead of high-credit single courses

Guidelines:
1. Each semester should have 15-20 total credits (achieved by having 4-6 courses per semester)
2. Include a mix of Core, Elective, and Lab courses
3. Ensure proper prerequisite chains
4. Progress from foundational to advanced topics
5. Include practical/project courses
6. Make course codes realistic (e.g., CS101, ML201)
7. Provide detailed course descriptions

Return ONLY the JSON object with no additional text, markdown formatting, or code blocks.
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
