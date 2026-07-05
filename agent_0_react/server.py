from os import name
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name="my-mcp-server")

# tool 1:
@mcp.tool
def add(a:int, b:int) -> int:
    """Add two numbers together"""
    return a + b

# tool 2:
@mcp.tool
def read_file(file_path:str) -> str:
    """Read a file and return the contents"""
    with open(file_path, "r") as file:
        return file.read()

if __name__ == "__main__":
    mcp.run()