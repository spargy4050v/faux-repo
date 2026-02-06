"""
Scenario-specific prompts for all 12 use cases
"""

# ==========================
# PROFESSOR SCENARIOS
# ==========================

def get_course_structure_prompt(
    course_name: str,
    level: str,
    duration_weeks: int,
    prerequisites: list = None,
    focus_areas: list = None
) -> str:
    """Generate comprehensive course structure"""
    
    prompt = f"""You are an expert curriculum designer. Create a detailed course structure for:

Course: {course_name}
Level: {level}
Duration: {duration_weeks} weeks
"""
    
    if prerequisites:
        prompt += f"Prerequisites: {', '.join(prerequisites)}\n"
    if focus_areas:
        prompt += f"Focus Areas: {', '.join(focus_areas)}\n"
    
    prompt += """
Generate a comprehensive course structure with:
1. Weekly breakdown with topics and subtopics
2. Learning objectives for each week
3. Assignments and projects
4. Assessment methods
5. Recommended resources

Return as JSON:
{
  "course_name": "string",
  "level": "string",
  "total_weeks": number,
  "weekly_structure": [
    {
      "week": 1,
      "topics": ["topic1", "topic2"],
      "learning_objectives": ["objective1"],
      "activities": ["activity1"],
      "assessments": ["assessment1"]
    }
  ],
  "course_outcomes": ["outcome1"],
  "prerequisites_validated": ["prereq1"],
  "recommended_resources": ["resource1"]
}

Use valid JSON only. Each course should align with industry standards and pedagogical best practices."""
    
    return prompt


def get_learning_outcome_mapping_prompt(
    course_content: str,
    competency_framework: str,
    academic_level: str
) -> str:
    """Map course content to learning outcomes"""
    
    return f"""You are an academic assessment expert. Map the following course content to specific learning outcomes using {competency_framework} framework.

Course Content:
{course_content}

Academic Level: {academic_level}

Generate learning outcome mappings with:
1. Specific, measurable learning outcomes (using Bloom's taxonomy)
2. Alignment with competency framework
3. Assessment methods for each outcome
4. Rubrics and evaluation criteria

Return as JSON:
{{
  "framework": "{competency_framework}",
  "learning_outcomes": [
    {{
      "outcome_id": "LO1",
      "description": "Students will be able to...",
      "cognitive_level": "Apply/Analyze/Create",
      "content_mapping": ["Topic X", "Topic Y"],
      "assessment_methods": ["method1"],
      "evaluation_criteria": ["criteria1"]
    }}
  ],
  "alignment_score": "High/Medium/Low",
  "recommendations": ["recommendation1"]
}}

Use valid JSON. Ensure outcomes are SMART (Specific, Measurable, Achievable, Relevant, Time-bound)."""


def get_curriculum_optimization_prompt(
    current_curriculum: str,
    optimization_goals: list,
    constraints: list = None
) -> str:
    """Optimize existing curriculum"""
    
    constraints_text = f"\nConstraints: {', '.join(constraints)}" if constraints else ""
    
    return f"""You are a curriculum optimization specialist. Analyze and optimize the following curriculum:

Current Curriculum:
{current_curriculum}

Optimization Goals: {', '.join(optimization_goals)}{constraints_text}

Provide:
1. Analysis of current curriculum strengths and weaknesses
2. Specific optimization recommendations
3. Updated curriculum structure
4. Expected improvements and metrics
5. Implementation roadmap

Return as JSON:
{{
  "analysis": {{
    "strengths": ["strength1"],
    "weaknesses": ["weakness1"],
    "gaps": ["gap1"]
  }},
  "recommendations": [
    {{
      "area": "string",
      "current_state": "string",
      "proposed_change": "string",
      "expected_impact": "string",
      "priority": "High/Medium/Low"
    }}
  ],
  "optimized_structure": {{}},
  "metrics": {{
    "predicted_improvement": "percentage",
    "areas": ["area1"]
  }},
  "implementation_plan": ["step1"]
}}

Use valid JSON. Focus on data-driven, evidence-based recommendations."""


def get_industry_alignment_prompt(
    curriculum_area: str,
    target_industry: str,
    job_roles: list = None
) -> str:
    """Analyze industry alignment"""
    
    roles_text = f" for roles: {', '.join(job_roles)}" if job_roles else ""
    
    return f"""You are an industry-academic liaison expert. Analyze how well a {curriculum_area} curriculum aligns with {target_industry} industry needs{roles_text}.

Provide:
1. Current industry skill demands
2. Gaps in curriculum vs industry needs
3. Emerging technologies and trends to include
4. Practical skills and tools students should learn
5. Industry certifications to integrate
6. Real-world project suggestions

Return as JSON:
{{
  "industry_skills_required": [
    {{
      "skill": "string",
      "importance": "Critical/High/Medium",
      "current_coverage": "Yes/Partial/No"
    }}
  ],
  "gaps_identified": ["gap1"],
  "emerging_trends": ["trend1"],
  "recommended_additions": [
    {{
      "topic": "string",
      "rationale": "string",
      "suggested_duration": "hours/weeks"
    }}
  ],
  "industry_tools": ["tool1"],
  "certifications": ["cert1"],
  "project_recommendations": ["project1"]
}}

Use valid JSON. Base recommendations on current 2024-2026 industry standards."""


def get_topic_recommendations_prompt(
    subject_area: str,
    current_topics: list,
    target_audience: str,
    timeframe: str = "next 2 years"
) -> str:
    """Generate topic recommendations"""
    
    return f"""You are a subject matter expert in {subject_area}. Recommend new topics that should be incorporated into the curriculum for {target_audience} relevant for {timeframe}.

Current Topics: {', '.join(current_topics)}

Provide:
1. Emerging topics in the field
2. Topics gaining industry traction
3. Foundational topics that may be missing
4. Advanced topics for differentiation
5. Interdisciplinary topics for broader learning

Return as JSON:
{{
  "recommended_topics": [
    {{
      "topic_name": "string",
      "category": "Emerging/Foundational/Advanced/Interdisciplinary",
      "relevance_score": 1-10,
      "rationale": "string",
      "prerequisites": ["prereq1"],
      "suggested_duration": "hours",
      "industry_demand": "High/Medium/Low",
      "learning_resources": ["resource1"]
    }}
  ],
  "topics_to_update": [
    {{
      "current_topic": "string",
      "suggested_updates": "string"
    }}
  ],
  "topics_to_remove": ["topic1"],
  "implementation_priority": ["topic1", "topic2", "topic3"]
}}

Use valid JSON. Focus on forward-looking, industry-relevant topics."""


def get_prerequisite_analysis_prompt(
    course_list: list,
    program_level: str
) -> str:
    """Analyze and structure prerequisites"""
    
    return f"""You are a curriculum architect. Analyze the following courses and create an optimal prerequisite structure for a {program_level} program:

Courses: {', '.join(course_list)}

Provide:
1. Prerequisite relationships between courses
2. Suggested course sequences/pathways
3. Parallel courses that can be taken together
4. Critical path analysis
5. Semester-wise breakdown

Return as JSON:
{{
  "prerequisite_map": {{
    "course_name": {{
      "prerequisites": ["course1"],
      "enables": ["course2"],
      "difficulty_level": 1-10,
      "semester_recommendation": number
    }}
  }},
  "learning_pathways": [
    {{
      "pathway_name": "string",
      "description": "string",
      "course_sequence": ["course1", "course2"]
    }}
  ],
  "semester_structure": {{
    "1": ["course1", "course2"],
    "2": ["course3"]
  }},
  "parallel_courses": [["course1", "course2"]],
  "critical_path": ["course1", "course2"],
  "warnings": ["warning1"]
}}

Use valid JSON. Ensure logical progression and avoid circular dependencies."""


# ==========================
# STUDENT SCENARIOS
# ==========================

def get_skill_gap_analysis_prompt(
    resume_text: str,
    target_role: str = None,
    job_description: str = None
) -> str:
    """Analyze skill gaps from resume"""
    
    comparison = f"\nTarget Role: {target_role}" if target_role else ""
    comparison += f"\nJob Description: {job_description}" if job_description else ""
    
    return f"""Analyze the following resume and identify skill gaps:{comparison}

Resume:
{resume_text}

Provide:
1. Current skills identified
2. Skill gaps for target role
3. Learning recommendations prioritized
4. Estimated time to acquire each skill
5. Resources and courses

Return as JSON:
{{
  "current_skills": [
    {{
      "skill": "string",
      "proficiency_level": "Beginner/Intermediate/Advanced/Expert",
      "evidence": "string from resume"
    }}
  ],
  "skill_gaps": [
    {{
      "skill": "string",
      "importance": "Critical/High/Medium/Low",
      "difficulty_to_acquire": "Easy/Medium/Hard",
      "estimated_time": "hours/weeks/months"
    }}
  ],
  "learning_roadmap": [
    {{
      "skill": "string",
      "priority": 1-10,
      "learning_path": ["step1", "step2"],
      "resources": ["resource1"],
      "estimated_duration": "string"
    }}
  ],
  "strengths": ["strength1"],
  "recommended_focus": ["skill1", "skill2", "skill3"]
}}

Use valid JSON. Be specific and actionable."""


def get_career_path_planner_prompt(
    current_position: str,
    target_role: str,
    timeframe: str,
    constraints: list = None
) -> str:
    """Create detailed career path"""
    
    constraints_text = f"\nConstraints: {', '.join(constraints)}" if constraints else ""
    
    return f"""Create a detailed career development plan:

Current Position: {current_position}
Target Role: {target_role}
Timeframe: {timeframe}{constraints_text}

Provide:
1. Career milestones and intermediate roles
2. Skills to develop at each stage
3. Certifications and education needed
4. Projects to build portfolio
5. Networking and experience recommendations
6. Timeline with actionable steps

Return as JSON:
{{
  "career_milestones": [
    {{
      "milestone": "string",
      "target_date": "string",
      "requirements": ["req1"],
      "deliverables": ["deliverable1"]
    }}
  ],
  "skill_development_plan": {{
    "technical_skills": ["skill1"],
    "soft_skills": ["skill1"],
    "tools_technologies": ["tool1"]
  }},
  "certifications": [
    {{
      "name": "string",
      "priority": "High/Medium/Low",
      "estimated_cost": "string",
      "estimated_time": "string",
      "when_to_pursue": "string"
    }}
  ],
  "portfolio_projects": ["project1"],
  "experience_recommendations": ["recommendation1"],
  "monthly_action_plan": {{
    "Month 1-3": ["action1"],
    "Month 4-6": ["action1"]
  }}
}}

Use valid JSON. Be realistic and specific."""


def get_job_opportunities_prompt(
    skills: list,
    interests: list,
    experience_level: str,
    location_preference: str = None
) -> str:
    """Recommend job opportunities"""
    
    location = f"\nLocation Preference: {location_preference}" if location_preference else "\nLocation: Remote/Flexible"
    
    return f"""Recommend suitable job opportunities based on:

Skills: {', '.join(skills)}
Interests: {', '.join(interests)}
Experience Level: {experience_level}{location}

Provide:
1. Matching job roles with fit scores
2. Required vs optional skills for each role
3. Typical salary ranges
4. Companies known for hiring in these roles
5. Job search strategies

Return as JSON:
{{
  "recommended_roles": [
    {{
      "job_title": "string",
      "match_score": 1-100,
      "required_skills": ["skill1"],
      "optional_skills": ["skill1"],
      "skills_you_have": ["skill1"],
      "skills_to_develop": ["skill1"],
      "typical_salary_range": "string",
      "growth_potential": "High/Medium/Low",
      "market_demand": "High/Medium/Low"
    }}
  ],
  "target_companies": ["company1"],
  "job_search_strategies": ["strategy1"],
  "networking_tips": ["tip1"],
  "interview_preparation": ["tip1"]
}}

Use valid JSON. Focus on realistic, achievable opportunities."""


def get_project_ideas_prompt(
    field: str,
    skill_level: str,
    interests: list,
    portfolio_goal: str
) -> str:
    """Generate project ideas"""
    
    return f"""Suggest industry-relevant project ideas:

Field: {field}
Skill Level: {skill_level}
Interests: {', '.join(interests)}
Portfolio Goal: {portfolio_goal}

Provide:
1. Project ideas ranked by complexity
2. Skills demonstrated by each project
3. Implementation guidelines
4. Technologies to use
5. Portfolio presentation tips

Return as JSON:
{{
  "projects": [
    {{
      "title": "string",
      "difficulty": "Beginner/Intermediate/Advanced",
      "estimated_duration": "hours/days/weeks",
      "skills_demonstrated": ["skill1"],
      "technologies": ["tech1"],
      "description": "string",
      "key_features": ["feature1"],
      "why_impactful": "string",
      "similar_industry_applications": ["app1"]
    }}
  ],
  "project_sequence": ["project1", "project2"],
  "portfolio_tips": ["tip1"],
  "presentation_guidelines": ["guideline1"]
}}

Use valid JSON. Focus on projects that demonstrate real-world problem-solving."""


def get_course_prerequisites_prompt(
    target_field: str,
    current_knowledge: list,
    learning_goal: str
) -> str:
    """Identify course prerequisites"""
    
    return f"""Identify the learning prerequisites needed:

Target Field: {target_field}
Current Knowledge: {', '.join(current_knowledge)}
Learning Goal: {learning_goal}

Provide:
1. Foundational knowledge required
2. Prerequisite courses in order
3. Self-study vs formal education recommendations
4. Estimated time for each prerequisite
5. Free vs paid resources

Return as JSON:
{{
  "foundational_knowledge": ["knowledge1"],
  "prerequisite_courses": [
    {{
      "course_name": "string",
      "level": "Beginner/Intermediate/Advanced",
      "why_needed": "string",
      "estimated_duration": "string",
      "recommended_providers": ["provider1"],
      "free_alternatives": ["alternative1"],
      "order": number
    }}
  ],
  "self_study_topics": ["topic1"],
  "total_estimated_time": "string",
  "learning_path_visual": "step1 -> step2 -> step3"
}}

Use valid JSON. Provide clear, sequential learning path."""


def get_industry_tools_prompt(
    industry_domain: str,
    role_type: str,
    current_tools_known: list = None
) -> str:
    """Recommend industry tools and technologies"""
    
    known = f"\nTools You Know: {', '.join(current_tools_known)}" if current_tools_known else ""
    
    return f"""Recommend essential industry tools and technologies:

Industry Domain: {industry_domain}
Role Type: {role_type}{known}

Provide:
1. Must-know tools categorized
2. Emerging tools gaining traction
3. Learning resources for each tool
4. Industry adoption levels
5. Free alternatives to paid tools

Return as JSON:
{{
  "essential_tools": [
    {{
      "tool_name": "string",
      "category": "string",
      "importance": "Critical/High/Medium",
      "industry_adoption": "percentage",
      "learning_curve": "Easy/Medium/Steep",
      "cost": "Free/Freemium/Paid",
      "alternatives": ["alt1"],
      "learning_resources": ["resource1"]
    }}
  ],
  "emerging_technologies": ["tech1"],
  "skill_combinations": [
    {{
      "combination": ["tool1", "tool2"],
      "use_case": "string"
    }}
  ],
  "learning_roadmap": {{
    "beginner": ["tool1"],
    "intermediate": ["tool2"],
    "advanced": ["tool3"]
  }}
}}

Use valid JSON. Focus on currently relevant tools (2024-2026)."""
