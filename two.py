from fastmcp import FastMCP
import yfinance as yf
from duckduckgo_search import DDGS
import json 

mcp = FastMCP("Wall Street Analyst")

watchlist = ["AAPL", "GOOGL"]

@mcp.tool 
def get_stock_data(ticker: str) -> str:
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # We extract only the most relevant data to keep context small
        data = {
            "symbol": ticker.upper(),
            "current_price": info.get("currentPrice"),
            "market_cap": info.get("marketCap"),
            "pe_ratio": info.get("trailingPE"),
            "recommendation": info.get("recommendationKey"),
            "business_summary": info.get("longBusinessSummary")[:200] + "..." # Truncate summary
        }
        return json.dumps(data, indent=2)
    except Exception as e:
        return f"Error fetching data for {ticker}: {str(e)}"
    
@mcp.tool()
def get_market_news(query: str) -> str:
    """
    Search for the latest financial news about a company or topic.
    """
    results = []
    # Use DuckDuckGo to search news
    with DDGS() as ddgs:
        # Get 3 latest news results
        for r in ddgs.news(query, max_results=3):
            results.append(f"Title: {r['title']}\nSource: {r['source']}\nLink: {r['url']}\n")
            
    return "\n---\n".join(results) if results else "No news found."

@mcp.resource("stock://watchlist")
def view_watchlist() -> str:
    """View the current user's stock watchlist."""
    return ", ".join(watchlist)

@mcp.tool()
def add_to_watchlist(ticker: str) -> str:
    """Add a stock ticker to the watchlist."""
    if ticker.upper() not in watchlist:
        watchlist.append(ticker.upper())
        return f"Added {ticker} to watchlist."
    return f"{ticker} is already in the watchlist."

if __name__ == "__main__":
    mcp.run()