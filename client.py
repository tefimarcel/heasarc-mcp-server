import asyncio
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


SERVER_COMMAND = ["python", "-m", "server.main"]


async def run_tool(tool_name: str, arguments: dict) -> str:
    """Connect to the MCP server and call a single tool."""
    server_params = StdioServerParameters(
        command=SERVER_COMMAND[0],
        args=SERVER_COMMAND[1:],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool(tool_name, arguments=arguments)
            return result.content[0].text


def print_usage():
    print("""
HEASARC MCP Client
==================

Usage:
  python client.py resolve <object_name>
  python client.py search <object_name> [mission] [min_exposure_ks]

Examples:
  python client.py resolve "Cas A"
  python client.py search "Cas A"
  python client.py search "Cas A" XMM
  python client.py search "Cas A" XMM 50
  python client.py search "Crab Nebula" all 10
""")


async def main():
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "resolve":
        if len(sys.argv) < 3:
            print("Usage: python client.py resolve <object_name>")
            sys.exit(1)
        object_name = sys.argv[2]
        print(f"Resolving '{object_name}'...")
        result = await run_tool("tool_resolve_object", {"object_name": object_name})
        print(result)

    elif command == "search":
        if len(sys.argv) < 3:
            print("Usage: python client.py search <object_name> [mission] [min_exposure_ks]")
            sys.exit(1)

        object_name = sys.argv[2]
        mission = sys.argv[3] if len(sys.argv) > 3 else "all"
        min_exposure_ks = float(sys.argv[4]) if len(sys.argv) > 4 else 0.0

        print(f"Searching observations for '{object_name}' | mission: {mission} | min exposure: {min_exposure_ks} ks\n")
        result = await run_tool(
            "tool_search_observations",
            {
                "object_name": object_name,
                "mission": mission,
                "min_exposure_ks": min_exposure_ks,
            }
        )
        print(result)

    else:
        print(f"Unknown command: '{command}'")
        print_usage()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
