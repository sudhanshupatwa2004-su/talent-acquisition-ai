import json
from crewai import Task


def create_tasks(agents, job_desc, candidates_data):
    """Create and return all 4 recruitment tasks."""

    sourcing_agent, screening_agent, engagement_agent, scheduling_agent = agents

    # Only pass name, skills, experience, education to keep prompts clean
    simplified = [
        {
            "name":       c["name"],
            "skills":     c["skills"],
            "experience": c["experience"],
            "education":  c["education"],
            "location":   c.get("location", "India"),
        }
        for c in candidates_data
    ]

    sourcing_task = Task(
        description=(
            f"Search for candidates for this job: {job_desc}\n"
            f"Available candidates from our database:\n"
            f"{json.dumps(simplified, indent=2)}\n\n"
            "Identify the top 4 most suitable candidates with brief reasons why they match."
        ),
        agent=sourcing_agent,
        expected_output="List of top 4 candidates with brief sourcing notes",
    )

    screening_task = Task(
        description=(
            f"Screen and rank ALL candidates for this job: {job_desc}\n"
            f"Candidates:\n{json.dumps(simplified, indent=2)}\n\n"
            "Score each candidate out of 100 using:\n"
            "- Skills match: 40 points\n"
            "- Years of experience: 30 points\n"
            "- Education relevance: 20 points\n"
            "- Cultural fit indicators: 10 points\n\n"
            "Return a ranked list with scores and 1-line justification for each."
        ),
        agent=screening_agent,
        expected_output="Ranked list of candidates with scores out of 100",
    )

    engagement_task = Task(
        description=(
            f"Write a professional, warm outreach email for the top candidate "
            f"for this role: {job_desc}.\n"
            "Keep it under 150 words. Include a subject line and email body. "
            "Make it feel human, not like a template."
        ),
        agent=engagement_agent,
        expected_output="Outreach email with subject line and body under 150 words",
    )

    scheduling_task = Task(
        description=(
            f"Create a detailed interview schedule for the top 3 candidates for: {job_desc}.\n"
            "Schedule interviews starting from tomorrow, one per day.\n"
            "Use these time slots: 10 AM, 2 PM, 4 PM.\n"
            "Include: Candidate name, Date, Time, Interviewer (use realistic Indian names), "
            "Interview mode (Video/In-person), and Round (Technical/HR/Final)."
        ),
        agent=scheduling_agent,
        expected_output="Formatted interview schedule table for top 3 candidates",
    )

    return [sourcing_task, screening_task, engagement_task, scheduling_task]