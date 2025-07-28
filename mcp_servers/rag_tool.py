# mcp_servers/rag_tool.py
from typing import ClassVar
from fastmcp.tools import Tool
from pydantic import Field
import os
from mcp_servers.nlp_utils import llama_rephrase, llama_generate_sql
from mcp_servers.sql_tool import SQLTool
from mcp_servers.validator import validate_sql

class RAGTool(Tool):
    key: ClassVar[str] = "rag_query"
    api_key: str = Field(default_factory=lambda: os.getenv("TOGETHER_API_KEY", ""), exclude=True)

    def __init__(self, sql_tool: SQLTool, api_key: str = None):
        super().__init__(
            name="RAGTool",
            description="Retrieve and generate answers from the employee database using SQL + LLaMA NLP.",
            parameters={
                "question": {
                    "type": "string",
                    "description": "The natural language question to answer."
                }
            },
        )
        object.__setattr__(self, "api_key", api_key or os.getenv("TOGETHER_API_KEY", ""))
        self._sql_tool = sql_tool

    async def run(self, question: str) -> dict:
        try:
            # ✅ Let LLaMA propose a SQL query
            sql_query = llama_generate_sql(question)

            # ✅ Validate query before running
            if not validate_sql(sql_query):
                return {"answer": "❌ Unsafe or invalid SQL generated."}

            # ✅ Run the SQL safely
            raw_result = await self._sql_tool.run(sql=sql_query)

            # ✅ Pass result + question to LLaMA for natural answer
            natural_answer = llama_rephrase(question, raw_result)
            return {"answer": natural_answer}

        except Exception as e:
            return {"error": f"❌ RAGTool failed: {e}"}
