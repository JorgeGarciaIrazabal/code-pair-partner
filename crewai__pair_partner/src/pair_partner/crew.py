import os
import sys

from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import FileReadTool, FileWriterTool, MCPServerAdapter
from mcp import StdioServerParameters

serverparams = StdioServerParameters(
    command=sys.executable,
    args=["/home/jorge/code/code-pair-partner/mcp_server.py"],
    env={"UV_PYTHON": "3.12", **os.environ},
)

mcp_server_adapter = MCPServerAdapter(serverparams)

@CrewBase
class PairPartner():
    """PairPartner crew"""

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def tester(self) -> Agent:
        return Agent(
            config=self.agents_config['tester'],
            verbose=True,
            llm=LLM(
                model="ollama/cogito:14b",
                api_base="http://localhost:11434",
                stream=True,
            )
        )

    @agent
    def local_file_manager(self) -> Agent:
        return Agent(
            config=self.agents_config['local_file_manager'],
            verbose=True,
            tools=[FileWriterTool(), FileReadTool()],
            llm=LLM(
                model="ollama/cogito:14b",
                api_base="http://localhost:11434",
                stream=True,
            )
        )

    @agent
    def math_expert(self) -> Agent:
        return Agent(
            config=self.agents_config['math_expert'],
            verbose=True,
            tools=mcp_server_adapter.tools,
            llm=LLM(
                model="ollama/cogito:14b",
                api_base="http://localhost:11434",
                stream=True,
            )
        )

    # @task
    # def read_content_from_file(self) -> Task:
    #     return Task(
    #         config=self.tasks_config['read_content_from_file'],
    #     )
    #
    # @task
    # def create_tests_for_features(self) -> Task:
    #     return Task(
    #         config=self.tasks_config['create_tests_for_features'],
    #     )
    #
    #
    # @task
    # def write_content_in_file(self) -> Task:
    #     return Task(
    #         config=self.tasks_config['write_content_in_file'],
    #     )

    @task
    def calculate(self) -> Task:
        return Task(
            config=self.tasks_config['calculate'],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the PairPartner crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
