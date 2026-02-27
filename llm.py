import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def build_prompt(schema_text: str, question: str) -> str:
    return f"""
You are a senior data analyst.

Convert the user's question into ONE valid SQL query.

STRICT RULES:
- Output ONLY SQL (no markdown, no explanation)
- Use ONLY tables and columns from the schema
- Only SELECT statements are allowed
- Do not hallucinate columns
- Prefer simple aggregations when appropriate

Schema:
{schema_text}

User question:
{question}
""".strip()

def question_to_sql(schema_text: str, question: str) -> str:
    prompt = build_prompt(schema_text, question)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You generate SQL only."},
            {"role": "user", "content": prompt},
        ],
        temperature=0
    )

    sql = response.choices[0].message.content.strip()
    return sql
