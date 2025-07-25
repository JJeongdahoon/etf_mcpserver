from mcp.server.fastmcp import FastMCP, Context
import httpx

# ✅ MCP 서버 이름을 바꿔줘
mcp = FastMCP("etfapi")

# ✅ ETF 목록 가져오기 툴
@mcp.tool()
async def get_etf_list(
    etf: str = None,
    ctx: Context = None
) -> str:
    """
    TIGER ETF Top10 API에서 ETF 목록을 가져오는 MCP 도구
    Args:
        etf: ETF 이름 일부로 필터링
    """
    base_url = "https://etfapi.onrender.com/etf"
    params = {}
    if etf:
        params["etf"] = etf
    async with httpx.AsyncClient() as client:
        resp = await client.get(base_url, params=params)
        resp.raise_for_status()
        data = resp.json()
        # 보기 좋게 포맷팅
        result = "# ETF 목록\n\n"
        for item in data:
            result += f"## {item['ETF']}\n"
            for stock in item['Top10']:
                result += f"- {stock['종목명']} ({stock['주식수']}주, {stock['구성비']}%)\n"
            result += "\n"
        return result.strip()

# ✅ 특정 ETF 상세 가져오기 툴
@mcp.tool()
async def get_etf_detail(
    etf_name: str,
    ctx: Context = None
) -> str:
    """
    TIGER ETF Top10 API에서 특정 ETF의 상세 Top10을 가져오는 MCP 도구
    Args:
        etf_name: ETF 이름 (예: TIGER_200)
    """
    url = f"https://etfapi.onrender.com/etf/{etf_name}"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        if resp.status_code == 404:
            return f"{etf_name} ETF를 찾을 수 없습니다."
        resp.raise_for_status()
        data = resp.json()
        result = f"# {data['ETF']} 상세 Top10\n\n"
        for stock in data['Top10']:
            result += f"- {stock['종목명']} ({stock['주식수']}주, {stock['구성비']}%)\n"
        return result.strip()

if __name__ == "__main__":
    mcp.run(transport="stdio")
