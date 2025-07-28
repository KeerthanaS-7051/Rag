# mcp_servers/validator.py

def validate_sql(sql: str) -> bool:
    """Allow only safe read-only SQL statements."""
    sql_lower = sql.lower().strip()
    return sql_lower.startswith("select") and not any(
        keyword in sql_lower for keyword in ["insert", "update", "delete", "drop", "alter"]
    )
