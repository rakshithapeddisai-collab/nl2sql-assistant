import os
import time
import streamlit as st
from openai import OpenAI
from openai import RateLimitError, APIError, APITimeoutError

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def build_prompt(schema_text: str, question: str) -> str:
    return f"""
You are a senior data analyst. Convert the user's question into ONE SQL query.

STRICT RULES:
- Output ONLY SQL (no markdown, no explanation)
- Use ONLY tables/columns from the schema
- SELECT-only
- If user asks for "total revenue", use SUM(revenue)
- Prefer simple aggregations

Schema:
{schema_text}

User question:
{question}
""".strip()

def _fallback_sql(question: str) -> str:
    q = (question or "").lower()
    if "total" in q and "revenue" in q:
        return "SELECT SUM(revenue) AS total_revenue FROM orders"
    if "monthly" in q and "revenue" in q:
        return """
        SELECT substr(order_date, 1, 7) AS month, SUM(revenue) AS revenue
        FROM orders
        GROUP BY substr(order_date, 1, 7)
        ORDER BY month
        """.strip()
    if "revenue" in q and "region" in q:
        return "SELECT region, SUM(revenue) AS revenue FROM orders GROUP BY region ORDER BY revenue DESC"
    return "SELECT * FROM orders LIMIT 20"

@st.cache_data(ttl=3600)  # cache results for 1 hour
def _cached_llm_sql(schema_text: str, question: str) -> str:
    prompt = build_prompt(schema_text, question)
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Return SQL only."},
            {"role": "user", "content": prompt},
        ],
        temperature=0,
    )
    return resp.choices[0].message.content.strip()

def question_to_sql(schema_text: str, question: str) -> str:
    # prevent empty calls
    if not (question or "").strip():
        return "SELECT * FROM orders LIMIT 20"

    # simple client-side throttle: prevents accidental rapid reruns
    now = time.time()
    last = st.session_state.get("_last_llm_call_ts", 0.0)
    if now - last < 2.0:
        # too soon; return cached/fallback
        return _fallback_sql(question)
    st.session_state["_last_llm_call_ts"] = now

    try:
        return _cached_llm_sql(schema_text, question)
    except (RateLimitError, APITimeoutError, APIError):
        # graceful degradation instead of crashing
        return _fallback_sql(question)
