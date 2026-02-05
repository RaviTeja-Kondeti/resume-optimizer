"""
Resume Optimizer Module
Uses Claude API to optimize resumes based on job descriptions
"""

import os
from anthropic import Anthropic
from typing import Dict, Optional


class ResumeOptimizer:
    """Optimize resumes using Claude AI"""

    def __init__(self):
        """Initialize Claude API client"""
        self.client = None
        self.api_key = os.getenv('ANTHROPIC_API_KEY')

    def _ensure_client(self):
        """Lazy initialization of Claude client"""
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables. Please add it to your .env file.")
        if self.client is None:
            self.client = Anthropic(api_key=self.api_key)

    def optimize_resume(
        self,
        resume_text: str,
        job_title: str,
        job_description: str
    ) -> Optional[Dict]:
        """
        Optimize resume based on job description

        Args:
            resume_text: Current resume content
            job_title: Target job title
            job_description: Job description to tailor resume for

        Returns:
            Dictionary with optimized resume sections or None if error
        """
        try:
            # Ensure client is initialized
            self._ensure_client()
            prompt = f"""You are an expert ATS (Applicant Tracking System) resume optimizer. Your task is to tailor the provided resume to match the job description and make it ATS-friendly.

**Job Title:** {job_title}

**Job Description:**
{job_description}

**Current Resume:**
{resume_text}

**CRITICAL INSTRUCTIONS - Follow ALL of these exactly:**

1. **Act as an expert ATS resume optimizer** - Your goal is to make this candidate the PERFECT match for this role
2. **Identify ALL key terms, skills, requirements, and technologies** from the job description
3. **Make it ATS-friendly** - Use proper keywords, formatting, and industry terminology that ATS systems scan for
4. **Start EVERY bullet point with a strong action verb** (Led, Developed, Implemented, Designed, Optimized, etc.)
5. **Format ALL bullet points in ATR (Action-Task-Result) format**: "Action verb + problem X, with Y tools/methods to achieve Z result"
6. **EVERY bullet point MUST include at least one numeric result/metric** (percentages, dollar amounts, time savings, user counts, etc.)
7. **Professional summary MUST be in bullet points** (4-7 concise, impactful points with metrics)
8. **Add MORE bullet points** that directly match the job description requirements - make them a perfect candidate
9. **Points should be substantial but concise** - Not too short (min 15 words) or too long (max 35 words)
10. **Modify job titles if needed** to better align with the target role they're applying for
11. **IMPORTANT: Add points, metrics, and achievements that match the JD regardless of what's in the original resume** - If the JD requires skills/experience, show them in the optimized resume with realistic metrics
12. **Make it interview-worthy** - This resume MUST pass ATS and get the candidate an interview
13. **Use job description keywords naturally** throughout the resume without keyword stuffing

**Output Format:**
Return the optimized resume in the following JSON structure:
{{
  "name": "Full Name",
  "contact": {{
    "email": "email@example.com",
    "phone": "phone number",
    "location": "City, State ZIP",
    "github": "github url",
    "linkedin": "linkedin url"
  }},
  "professional_summary": [
    "Summary point 1 with specific achievement and metric",
    "Summary point 2 with specific achievement and metric",
    ...
  ],
  "professional_experience": [
    {{
      "job_title": "Job Title",
      "company": "Company Name",
      "location": "Location",
      "dates": "Date Range",
      "achievements": [
        "Achievement 1 in ATR format with numeric results",
        "Achievement 2 in ATR format with numeric results",
        ...
      ]
    }}
  ],
  "education": [
    {{
      "degree": "Degree Name",
      "institution": "Institution Name",
      "location": "Location",
      "dates": "Date Range",
      "details": ["Detail 1", "Detail 2"]
    }}
  ],
  "skills": {{
    "technical": ["skill1", "skill2", ...],
    "tools": ["tool1", "tool2", ...],
    "other": ["skill1", "skill2", ...]
  }},
  "certifications": [
    "Certification 1",
    "Certification 2"
  ]
}}

**REMEMBER:**
- This resume MUST pass ATS systems and get an interview
- Add more bullet points with strong metrics that match the JD requirements
- Every point needs a numeric result (%, $, time, count, etc.)
- Make the candidate look like the PERFECT fit for this exact role
- It's okay to enhance and expand on their experience to match the JD better

Return ONLY the JSON structure, no additional text or explanation."""

            message = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=8000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            # Extract the response content
            response_text = message.content[0].text

            # Parse JSON response
            import json
            optimized_data = json.loads(response_text)

            return optimized_data

        except Exception as e:
            print(f"Error optimizing resume: {e}")
            return None
