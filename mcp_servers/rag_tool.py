from typing import ClassVar
from fastmcp.tools import Tool
from pydantic import Field
import os
from mcp_servers.nlp_utils import llama_rephrase, llama_generate_sql
from mcp_servers.sql_tool import SQLTool

class RAGTool(Tool):
    key: ClassVar[str] = "rag_query"
    api_key: str = Field(default_factory=lambda: os.getenv("TOGETHER_API_KEY", ""), exclude=True)

    def __init__(self, sql_tool: SQLTool, session_memories: dict, api_key: str = None):
        super().__init__(
            name="RAGTool",
            description="Retrieve and generate answers from the employee database using SQL + LLaMA NLP.",
            parameters={
                "question": {"type": "string", "description": "The natural language question"},
                "session_id": {"type": "string", "description": "Unique session identifier"}
            },
        )
        object.__setattr__(self, "api_key", api_key or os.getenv("TOGETHER_API_KEY", ""))
        self._sql_tool = sql_tool
        self._session_memories = session_memories  

    async def run(self, question: str, session_id: str) -> dict:
        try:
            memory = self._session_memories.setdefault(session_id, [])

            sql_query = llama_generate_sql(question, memory)
            raw_result = await self._sql_tool.run(sql=sql_query)

            natural_answer = llama_rephrase(question, raw_result, memory)

            answer = natural_answer if natural_answer else "No answer generated."

            memory.append({"role": "user", "content": question})
            memory.append({"role": "assistant", "content": answer})

            return {"answer": answer}
        except Exception as e:
            return {"answer": f"RAGTool failed: {e}"}
