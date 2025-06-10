from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.tools import tool
import pandas as pd
from typing import List
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators


@tool("Read the starting 20 rows of excel file and store into dataframe using pandas")
def read_file():
    """
    Read the starting 20 rows of excel file and store into dataframe using pandas
    """
    df = pd.read_excel("src/hassan/Amazon_Trading.xlsx").head(30)
    shared_memory = {"data": df}
    return shared_memory

@CrewBase
class Hassan():
    """Hassan crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def query_interpreter(self) -> Agent:
        return Agent(
            config=self.agents_config['query_interpreter'], # type: ignore[index]
            verbose=True,
            allow_delegation=True,
        )

    @agent
    def strategic_planner(self) -> Agent:
        return Agent(
            config=self.agents_config['strategic_planner'], # type: ignore[index]
            verbose=True,
            allow_delegation=True,
        )


    @agent
    def data_analyzer(self) -> Agent:
        return Agent(
            config=self.agents_config['data_analyzer'], # type: ignore[index]
            verbose=True,
            tools=[read_file],
            allow_delegation=True,
        )

    @agent
    def responder(self) -> Agent:
        return Agent(
            config=self.agents_config['responder'], # type: ignore[index]
            verbose=True,
            allow_delegation=True,
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def interpret_query(self) -> Task:
        return Task(
            config=self.tasks_config['interpret_query'], # type: ignore[index]
        )


    @task
    def validate_plan(self) -> Task:
        return Task(
            config=self.tasks_config['validate_plan'], # type: ignore[index]
        )

    @task
    def analyze_data(self) -> Task:
        return Task(
            config=self.tasks_config['analyze_data'], # type: ignore[index]
            output_file='report.md'
        )

    @task
    def format_response(self) -> Task:
        return Task(
            config=self.tasks_config['format_response'], # type: ignore[index]
            output_file='report.md'
        )
        
    
    @crew
    def crew(self) -> Crew:
        """Creates the Hassan crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )