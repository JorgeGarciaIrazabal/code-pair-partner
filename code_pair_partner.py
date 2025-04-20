from crewai import Agent, Task, Crew
from mcp_tools import mcp


def create_file_agentic_flow() -> Crew:
    # Create an MCPTool that wraps the MCP instance defined in mcp_tools.py
    file_creation_tool = MCPTool(mcp, tool_name="create_file")

    file_creator_agent = Agent(
        role="File Creation Specialist",
        goal="Create files at given paths with specified content, handling file system appropriately.",
        backstory="Experienced in careful file creation and management with safety and correctness in mind.",
        verbose=True,
        tools=[file_creation_tool]
    )

    file_creation_task = Task(
        description="Create file with specified content and path",
        expected_output="Confirmation message of file creation success",
        agent=file_creator_agent
    )

    crew = Crew(
        agents=[file_creator_agent],
        tasks=[file_creation_task],
        verbose=True
    )
    return crew
