def validate_sql(sql: str) -> bool:
    sql_lower = sql.lower().strip()
    return sql_lower.startswith("select") and not any(
        keyword in sql_lower for keyword in ["insert", "update", "delete", "drop", "alter"]
    )
