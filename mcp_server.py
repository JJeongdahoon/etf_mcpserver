from mcp.server.fastmcp import FastMCP, Context
import httpx

mcp = FastMCP("etfapi")

ASK_URL = "https://etfapi.onrender.com/ask"

@mcp.tool()
async def ask_etfapi(
    query: str,
    ctx: Context = None
) -> str:
    """
    etfapi 서버의 /ask 엔드포인트로 쿼리를 보내고 답변을 가져오는 MCP 툴
    Args:
        query: 사용자가 묻고 싶은 내용 (ETF 이름 포함)
    """
    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            resp = await client.post(ASK_URL, json={"query": query})
            resp.raise_for_status()
            data = resp.json()
    except Exception as e:
        return f"❌ etfapi 호출 중 오류 발생: {e}"

    # 응답 검증
    if not isinstance(data, dict) or "answer" not in data:
        return "❌ etfapi에서 예상치 못한 응답을 받았습니다."

    # 최종 답변
    answer = data.get("answer", "")
    return answer.strip()

if __name__ == "__main__":
    mcp.run(transport="stdio")
