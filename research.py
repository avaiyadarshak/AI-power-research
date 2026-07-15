import os
import streamlit as st
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

try:
    tavily_api_key = st.secrets["TAVILY_API_KEY"]
except Exception:
    tavily_api_key = os.getenv("TAVILY_API_KEY")

tavily_client = TavilyClient(
    api_key=tavily_api_key
)


def research_company(company_name):

    queries = [
        f"{company_name} company overview industry operations geographic presence",
        f"{company_name} latest news recent developments 2026",
        f"{company_name} expansion plans business strategy",
        f"{company_name} products services major offerings",
        f"{company_name} business challenges customer complaints operational challenges"
    ]

    research_data = []

    for query in queries:

        try:
            response = tavily_client.search(
                query=query,
                search_depth="advanced",
                max_results=5
            )

            for result in response.get("results", []):
                research_data.append({
                    "title": result.get("title", ""),
                    "content": result.get("content", ""),
                    "url": result.get("url", "")
                })

        except Exception as e:
            print(f"Search error: {e}")

    return research_data
