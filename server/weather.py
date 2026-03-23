from typing import Any,Dict
import aiohttp
from mcp.server import FastMCP


# Initialize FastMCP server
mcp=FastMCP("weather")


# Constants
NWS_API_BASE="https://api.weather.gov"
USER_AGENT="weather-app/1.0" 

async def make_nws_request(url:str)->Dict[str,Any] | None:
    """Make a request to the NWS API with proper error handling"""
    headers={
        "User-Agent":USER_AGENT,
        "Accept":"application/geo+json"
    }
    timeout=aiohttp.ClientTimeout(total=30)
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url,headers=headers,timeout=timeout) as response: #type: ignore
                response.raise_for_status()
                return await response.json()
            
        except Exception as e:
            print(f"NWS request failed: {e}")
            return None
                



def format_alert(feature:dict)->str:
    """Format an alert feature into a readabble string"""
    props = feature.get("properties", {})
    return f"""
        Event:{props.get("event",'Unknown')}
        Area:{props.get("areaDesc",'Unknown')}
        Severity:{props.get("severity",'Unknown')}
        Description:{props.get("description",'No description provided ')}
        Instructions:{props.get("instruction",'No instructions provided ')}
            """




@mcp.tool()
async def get_alerts(state:str)->str:
    """Get weather alertss for a US state.
        Args:
        state:Two-lette US state code (e.g. CA,NY)
    """
    url=f"{NWS_API_BASE}/alerts/active/area/{state}"
    data=await make_nws_request(url=url)

    if not data or "features" not in data:
        return "Unable to fetch  alerts or no alerts found"
    
    if not data["features"]:
        return "No active alerts for this state. "
    
    alerts=[format_alert(feature) for feature in data["features"]]
    return "\n---\n".join(alerts)


if __name__ == "__main__":
    mcp.run()