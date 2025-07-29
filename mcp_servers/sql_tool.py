import sqlite3
from typing import ClassVar
from fastmcp.tools import Tool
from pydantic import Field
from mcp_servers.validator import validate_sql

class SQLTool(Tool):
    key: ClassVar[str] = "sql_query"
    db_path: str = Field(default="employees.db", exclude=True)

    def __init__(self, db_path: str = "employees.db"):
        super().__init__(
            name="SQLTool",
            description="Execute safe SQL SELECT queries on the employees database.",
            parameters={"sql": {"type": "string", "description": "The SQL SELECT query to execute"}},
        )
        object.__setattr__(self, "db_path", db_path)

    async def run(self, sql: str) -> dict:
        if not validate_sql(sql):
            return {"results": [], "error": "Unsafe query detected. Only SELECT is allowed."}
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()
            col_names = [desc[0] for desc in cursor.description]
            conn.close()

            if not rows:
                return {"results": [], "message": "No results found."}

            return {"columns": col_names, "rows": rows}

        except Exception as e:
            return {"results": [], "error": f"SQL execution failed: {e}"}
