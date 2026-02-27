def question_to_sql(schema_text: str, question: str) -> str:
    q = (question or "").strip().lower()

    if not q:
        return "SELECT * FROM orders LIMIT 20"

    # Monthly revenue trend
    if "monthly" in q and "revenue" in q:
        return """
        SELECT substr(order_date, 1, 7) AS month,
               SUM(revenue) AS revenue
        FROM orders
        GROUP BY substr(order_date, 1, 7)
        ORDER BY month
        """.strip()

    # Revenue by region
    if "revenue" in q and "region" in q:
        return """
        SELECT region,
               SUM(revenue) AS revenue
        FROM orders
        GROUP BY region
        ORDER BY revenue DESC
        """.strip()

    # Revenue by product
    if "revenue" in q and "product" in q:
        return """
        SELECT product,
               SUM(revenue) AS revenue
        FROM orders
        GROUP BY product
        ORDER BY revenue DESC
        """.strip()

    # Top N orders by revenue
    if "top" in q and "revenue" in q:
        return """
        SELECT order_id, order_date, region, product, revenue
        FROM orders
        ORDER BY revenue DESC
        LIMIT 10
        """.strip()

    # Default fallback
    return "SELECT * FROM orders LIMIT 20"
