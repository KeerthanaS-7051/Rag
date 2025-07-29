from typing import ClassVar
from fastmcp.tools import Tool
from pydantic import Field
import os
from mcp_servers.nlp_utils import llama_rephrase, llama_generate_sql
from mcp_servers.sql_tool import SQLTool

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
            sql_query = llama_generate_sql(question)
            raw_result = await self._sql_tool.run(sql=sql_query)
            if "answer" in raw_result:
                return {"answer": raw_result["answer"]}
            natural_answer = llama_rephrase(question, raw_result)
            return {"answer": natural_answer or "I could not generate a natural response."}

        except Exception as e:
            return {"answer": f"Server error in RAGTool: {e}"}
