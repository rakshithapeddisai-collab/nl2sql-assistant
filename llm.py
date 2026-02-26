def build_prompt(schema_text: str, question: str) -> str:
    return f"""
You are a helpful data analyst. Convert the user question into ONE SQL query.
Rules:
- Output ONLY SQL (no markdown).
- Use ONLY tables/columns from the schema.
- SELECT-only. No data changes.
- Prefer simple, correct SQL.

Schema:
{schema_text}

Question:
{question}
""".strip()

def call_llm(prompt: str) -> str:
    # TODO: Replace with your LLM call (OpenAI / Gemini / Claude / local model).
    # Return raw SQL string.
    raise NotImplementedError("Connect your LLM provider here.")

def question_to_sql(schema_text: str, question: str) -> str:
    prompt = build_prompt(schema_text, question)
    sql = call_llm(prompt)
    return (sql or "").strip()
