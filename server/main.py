from mcp.server.fastmcp import FastMCP
from server.tools.search import resolve_object, search_observations

mcp = FastMCP("HEASARC MCP Server")


@mcp.tool()
def tool_resolve_object(object_name: str) -> str:
    """
    Resolve an astronomical object name to RA/Dec coordinates.
    Example: 'Cas A', 'Crab', 'NGC 1234'
    """
    result = resolve_object(object_name)
    if "error" in result:
        return f"Error: {result['error']}"
    return result["message"]


@mcp.tool()
def tool_search_observations(
    object_name: str,
    mission: str = "all",
    min_exposure_ks: float = 0.0,
    max_results: int = 100
) -> str:
    """
    Search HEASARC for observations of an astronomical object.

    - object_name: name of the object (e.g. 'Cas A', 'Crab Nebula')
    - mission: 'XMM', 'Chandra', 'NuSTAR', 'NICER', or 'all'
    - min_exposure_ks: minimum exposure time in kiloseconds
    - max_results: maximum results per mission (default 100)
    """
    results = search_observations(object_name, mission, min_exposure_ks, max_results)

    if "error" in results:
        return f"Error: {results['error']}"

    output = []
    for mission_name, obs_list in results.items():
        if isinstance(obs_list, dict) and "error" in obs_list:
            output.append(f"{mission_name}: Error - {obs_list['error']}")
            continue
        if not obs_list:
            output.append(f"{mission_name}: no observations found")
            continue

        output.append(f"\n{mission_name} ({len(obs_list)} observations):")
        for obs in obs_list:
            line = f"  - {obs['obs_id']} | {obs['exposure_ks']} ks"
            # Append extra columns if present
            extras = {k: v for k, v in obs.items()
                      if k not in ("obs_id", "exposure_ks", "mission")}
            if extras:
                extra_str = " | ".join(f"{k}: {v}" for k, v in extras.items())
                line += f" | {extra_str}"
            output.append(line)

    return "\n".join(output)


if __name__ == "__main__":
    mcp.run()
