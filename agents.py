from crewai import Agent


def create_agents(llm):
    """Create and return all 4 recruitment AI agents."""

    sourcing_agent = Agent(
        role="Talent Sourcing Specialist",
        goal="Source the best candidates from job platforms and databases for the given job description",
        backstory=(
            "You are an expert talent sourcer with 10 years of experience. "
            "You know how to find hidden talent across LinkedIn, Naukri, "
            "GitHub and internal databases."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )

    screening_agent = Agent(
        role="Resume Screening Expert",
        goal="Analyze and screen resumes to find the best fit candidates based on skills, experience, and job requirements",
        backstory=(
            "You are an NLP expert in HR tech. You analyze resumes deeply, "
            "understand skill gaps, and rank candidates objectively."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )

    engagement_agent = Agent(
        role="Candidate Engagement Specialist",
        goal="Draft personalized outreach messages to engage top candidates professionally",
        backstory=(
            "You are a communication expert who writes compelling, warm, "
            "and professional messages that get responses from top candidates."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )

    scheduling_agent = Agent(
        role="Interview Scheduling Coordinator",
        goal="Create a structured interview schedule for shortlisted candidates",
        backstory=(
            "You are an organisational expert who creates efficient, "
            "conflict-free interview schedules that respect everyone's time."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )

    return sourcing_agent, screening_agent, engagement_agent, scheduling_agent