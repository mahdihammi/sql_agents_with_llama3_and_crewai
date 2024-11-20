from crewai import Agent, Crew, Process, Task
from textwrap import dedent
from tools import tables_schema, execute_sql, list_tables
from dotenv import load_dotenv
import os
from crewai import LLM


load_dotenv()
os.environ['GROQ_API_KEY'] = os.getenv("GROQ_API_KEY")

llm = LLM(
    model="groq/llama3-8b-8192",
    temperature=0
)

sql_dev = Agent(
    role="Senior Database Developer",
    goal="Construct and execute SQL queries based on a request",
    backstory=dedent(
    """
        You are an experienced database engineer who is master at creating efficient and complex SQL queries.
        You have a deep understanding of how different databases work and how to optimize queries.
        Use the `list_tables` to find available tables.
        Use the `tables_schema` to understand the metadata for the tables.
        Use the `execute_sql` to check your queries for correctness.

    """
    ),
    llm=llm,
    tools=[list_tables, tables_schema, execute_sql],
    allow_delegation=False,
)


data_analyst = Agent(
    role="Senior Data Analyst",
    goal="You receive data from the database developer and analyze it",
    backstory= dedent(
        """
        You have deep experience with analyzing datasets using Python.
        Your work is always based on the provided data and is clear,
        easy-to-understand and to the point. You have attention
        to detail and always produce very detailed work (as long as you need).
    """
    ),
    llm=llm,
    allow_delegation=False,
)


report_writer = Agent(
    role="Senior Report Editor",
    goal="Write an executive summary type of report based on the work of the analyst",
    backstory=dedent(
        """
        Your writing still is well known for clear and effective communication.
        You always summarize long texts into bullet points that contain the most
        important details and insights.
        """
    ),
    llm=llm,
    allow_delegation=False,
)
