import sys
import os
os.system('chcp 65001')  # Set console to UTF-8
sys.stdout.reconfigure(encoding='utf-8')

from phi.agent import Agent
from phi.model.groq import Groq
from phi.model.vertexai import Gemini
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo
from dotenv import load_dotenv

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
google_api_key = os.getenv("GOOGLE_API_KEY")

web_search_Agent = Agent(
    name="web_search",
    role="A helpful assistant that can search the web and return the results",
    tools=[DuckDuckGo()],
    model=Groq(api_key=groq_api_key, id="llama-3.3-70b-versatile", model_type="chat"),
    instruction=["Always provide the source"],
    show_tools_calls=True,
    markdown=True,
) 

# Financial Analysis Agent
financial_analysis_Agent = Agent(
    name="financial_analysis",
    role="A helpful assistant that can analyze financial data",
    model=Gemini(api_key=google_api_key, id="gemini-1.5-pro", model_type="chat"),
    tools=[
        YFinanceTools(stock_price=True, analyst_recommendations=True, key_financial_ratios=True, company_news=True),
    ], 
    instruction=["Use table to show the financial data"],
    show_tools_calls=True,
    markdown=True
)

multi_model_Agent = Agent(
   teams=[web_search_Agent, financial_analysis_Agent],
   instructions=["Always provide the source","Use table to show the financial data"], 
   show_tools_calls=True,
   markdown=True,
   model=Groq(api_key=groq_api_key, id="llama-3.3-70b-versatile", model_type="chat")  # Explicitly set model for multi-agent
)

multi_model_Agent.print_response(
    "Summerize the recent news about Tesla and share the stock price analysis and recommendation", stream=True 
)
