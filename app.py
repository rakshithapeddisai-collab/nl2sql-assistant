import streamlit as st
import pandas as pd
from db import get_engine, run_query
from llm import question_to_sql
from sql_guard import is_select_only

st.set_page_config(page_title="NLP to SQL Assistant", layout="wide")
st.title("NLP ➜ SQL Analytics Assistant")
st.caption("Tip: Click once. The app may take a second to generate SQL.")

st.write("Ask questions in plain English. The app generates SQL, runs it, and shows results.")

db_url = "sqlite:///sales.db"

schema_text = st.text_area(
    "Schema (used by the AI model)",
    value="Table: orders(order_id, order_date, region, product, revenue, quantity)",
    height=120
)

question = st.text_input("Your question", placeholder="Example: Show monthly revenue")

if st.button("Generate & Run"):
    sql = question_to_sql(schema_text, question)

    st.subheader("Generated SQL")
    st.code(sql, language="sql")

    if not is_select_only(sql):
        st.error("Blocked: SQL must be SELECT-only.")
        st.stop()

    engine = get_engine(db_url)
    df = run_query(engine, sql)

    st.subheader("Results")
    st.dataframe(df, use_container_width=True)

    # Basic chart if 2 columns
    if df.shape[1] == 2:
        try:
            df2 = df.copy()
            df2[df2.columns[1]] = pd.to_numeric(df2[df2.columns[1]], errors="coerce")
            if df2[df2.columns[1]].notna().any():
                st.line_chart(df2.set_index(df2.columns[0]))
        except Exception:
            pass
