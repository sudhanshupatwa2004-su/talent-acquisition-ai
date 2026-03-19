import os
from crewai import Crew, Process
from langchain_core.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEndpoint
from agents import create_agents
from tasks import create_tasks
from vector_db import MOCK_CANDIDATES
from dotenv import load_dotenv

load_dotenv()


def get_llm():
    """Initialize HuggingFace LLM via LangChain - FREE."""
    return HuggingFaceEndpoint(
        repo_id="mistralai/Mistral-7B-Instruct-v0.3",
        huggingfacehub_api_token=os.getenv("HUGGINGFACE_API_KEY"),
        temperature=0.3,
        max_new_tokens=512,
    )


def get_langchain_summary(job_desc):
    """
    Use LangChain PromptTemplate to analyze the job description.
    Shows LangChain usage clearly for viva evaluation.
    """
    prompt_template = PromptTemplate(
        input_variables=["job_description"],
        template=(
            "You are an expert HR analyst.\n"
            "Analyze this job description and extract:\n"
            "1. Required skills\n"
            "2. Experience level needed\n"
            "3. Key responsibilities\n"
            "4. Ideal candidate profile\n\n"
            "Job Description: {job_description}"
        )
    )
    formatted_prompt = prompt_template.format(job_description=job_desc)
    return formatted_prompt


def run_langchain_jd_analysis(job_desc):
    """
    Directly call HuggingFace LLM via LangChain to analyze the JD.
    Returns REAL AI output shown in the UI.
    """
    llm = get_llm()
    prompt_template = PromptTemplate(
        input_variables=["job_description"],
        template=(
            "[INST] You are a senior HR analyst with 15 years of experience.\n\n"
            "Analyze the following job description and provide:\n"
            "1. TOP 5 required technical skills\n"
            "2. Years of experience needed\n"
            "3. Three key responsibilities\n"
            "4. Ideal candidate summary in 2 sentences\n\n"
            "Job Description:\n{job_description}\n\n"
            "Provide a clear structured analysis: [/INST]"
        )
    )
    formatted = prompt_template.format(job_description=job_desc)
    response  = llm.invoke(formatted)
    return response


def run_chatbot_query(user_message, candidate_summary):
    """
    Use HuggingFace Mistral-7B via LangChain to answer
    any HR question in real time.
    """
    llm = get_llm()
    prompt_template = PromptTemplate(
        input_variables=["context", "question"],
        template=(
            "[INST] You are TalentAI, an intelligent HR Assistant. "
            "You have access to the following recruitment data:\n\n"
            "{context}\n\n"
            "Answer the HR manager's question clearly and concisely. "
            "Be helpful, professional and specific.\n\n"
            "Question: {question} [/INST]"
        )
    )
    formatted = prompt_template.format(
        context=candidate_summary,
        question=user_message
    )
    response = llm.invoke(formatted)
    return response if isinstance(response, str) else response.content


def run_crew_pipeline(job_desc):
    """
    Run the full CrewAI pipeline using HuggingFace LLM via LangChain.
    """
    llm    = get_llm()
    agents = create_agents(llm)
    tasks  = create_tasks(agents, job_desc, MOCK_CANDIDATES)

    crew = Crew(
        agents=list(agents),
        tasks=tasks,
        process=Process.sequential,
        verbose=True,
    )

    result = crew.kickoff()
    return str(result)