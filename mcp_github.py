# basic import
from mcp.server.fastmcp import FastMCP
import os
from github import Github
from dotenv import load_dotenv

load_dotenv(".env")


# instantiate an MCP server client
mcp = FastMCP("github_manager")

# GitHub authentication
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
# Obtain your GitHub API token by:
# 1. Going to https://github.com/settings/tokens
# 2. Clicking "Generate new token"
# 3. Selecting the necessary scopes (e.g., repo, user)
# 4. Copying the generated token
# Save this token in your environment variables as GITHUB_TOKEN

# instantiate an MCP server client
mcp = FastMCP("github_manager")

# GitHub authentication
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    raise RuntimeError("GITHUB_TOKEN environment variable not set")
gh = Github(GITHUB_TOKEN)
if not GITHUB_TOKEN:
    raise RuntimeError("GITHUB_TOKEN environment variable not set")
gh = Github(GITHUB_TOKEN)

# DEFINE TOOLS

@mcp.tool()
def list_my_repos() -> list:
    """List all repositories owned by the authenticated user."""
    user = gh.get_user()
    return [repo.full_name for repo in user.get_repos(affiliation="owner")]

@mcp.tool()
def repos_with_pyproject() -> list[str]:
    """
    List all repositories owned by the authenticated user that have a pyproject.toml in the root folder.
    """
    user = gh.get_user()
    repos:list[str] = []
    for repo in user.get_repos(affiliation="owner"):
        try:
            repo.get_contents("pyproject.toml")
            repos.append(repo.full_name)
        except Exception:
            continue
    return repos

@mcp.tool()
def get_file_content(repo_full_name: str, file_path: str) -> str:
    """
    Get the content of a file in a repository.
    Args:
        repo_full_name: e.g. "username/reponame"
        file_path: path to the file in the repo, e.g. "pyproject.toml"
    """
    repo = gh.get_repo(repo_full_name)
    file_content = repo.get_contents(file_path)
    return file_content.decoded_content.decode()

# execute and return the stdio output
if __name__ == "__main__":
    # mcp.run(transport="stdio")
    mcp.run(transport="sse")

