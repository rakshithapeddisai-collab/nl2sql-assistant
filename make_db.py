import sqlite3
import pandas as pd

conn = sqlite3.connect("sales.db")

df_orders = pd.DataFrame({
    "order_id": [1,2,3,4,5,6],
    "order_date": ["2025-01-05","2025-01-18","2025-02-02","2025-02-20","2025-03-01","2025-03-15"],
    "region": ["East","West","East","South","West","East"],
    "product": ["A","B","A","C","B","C"],
    "revenue": [1200, 2200, 800, 1500, 2600, 1700],
    "quantity": [3, 4, 2, 3, 5, 2]
})

df_orders.to_sql("orders", conn, index=False, if_exists="replace")
conn.close()

print("Created sales.db with table: orders")
