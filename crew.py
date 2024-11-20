from crewai import Agent, Crew, Process, Task
from agents import sql_dev, data_analyst, report_writer
from textwrap import dedent
from tasks import extract_data, analyze_data, write_report
from dotenv import load_dotenv

# mahdi hammi
load_dotenv()
crew = Crew(
    agents=[sql_dev, data_analyst, report_writer],
    tasks=[extract_data, analyze_data, write_report],
    process=Process.sequential,
    verbose=True,
    memory=False,
    output_log_file="crew.log",
)

#inputs = {
#  "query": "Effects on salary (in USD) based on company location, size and employee experience"
#}

#result = crew.kickoff(inputs=inputs)

#print(result)