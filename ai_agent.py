import os
import streamlit as st
from google import genai
from dotenv import load_dotenv

load_dotenv()

# Get API key from Streamlit Secrets or local .env
try:
    gemini_api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    gemini_api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(
    api_key=gemini_api_key
)

def generate_report(company_name, research_data):

    research_text = ""

    for item in research_data:
        research_text += f"""
Title: {item['title']}
Information: {item['content']}
Source: {item['url']}
"""

    prompt = f"""
You are an AI Business Research and Recommendation Agent.

Your task is to analyze the company:

Company Name: {company_name}

Below is research collected from web sources:

{research_text}

Generate a detailed but concise intelligence report.

IMPORTANT INSTRUCTIONS:

- Base factual claims on the supplied research.
- Clearly distinguish facts from your own analysis.
- Do not invent company information.
- Recommendations must be specific to {company_name}.
- Explain the reasoning behind identified challenges.
- Include relevant source URLs in the report.

Create the report using the following structure:

# 1. Company Overview

Explain:
- What the company does
- Industry
- Scale
- Geographic presence

# 2. Key Business Information

Explain:
- Major offerings
- Recent developments
- Expansion plans
- Important public information

# 3. Potential Business Challenges

Identify:
- Operational challenges
- Sales challenges
- Customer experience challenges
- Other potential bottlenecks

For every challenge, explain why you identified it.

# 4. AI Opportunities

Suggest practical and company-specific AI solutions.

For each opportunity explain:

Problem:
AI Solution:
How It Works:
Expected Business Impact:

Focus on areas such as:
- Automation
- Customer engagement
- Sales
- Operations
- Analytics
- Document processing

Avoid generic recommendations.

# 5. Personalized CEO Pitch

Write a professional one-page pitch addressed to the CEO.

Explain:
- Why we reached out
- Opportunities identified
- Recommended AI solutions
- Expected business impact

# 6. Sources

List the important sources used for the research.
"""

    response = client.models.generate_content(
       model="gemini-3-flash-preview",
        contents=prompt
    )

    return response.text
