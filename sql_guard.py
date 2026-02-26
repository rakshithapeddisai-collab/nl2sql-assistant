import re
import sqlparse

FORBIDDEN = {"insert", "update", "delete", "drop", "alter", "truncate", "create", "grant", "revoke"}

def is_select_only(sql: str) -> bool:
    if not sql or not sql.strip():
        return False
    statements = [s for s in sqlparse.split(sql) if s.strip()]
    if len(statements) != 1:
        return False

    s = statements[0].strip().lower()
    if not (s.startswith("select") or s.startswith("with")):
        return False

    tokens = re.findall(r"[a-zA-Z_]+", s)
    return not any(t in FORBIDDEN for t in tokens)
