from fastapi import FastAPI, Request
from fastmcp import FastMCP
from mcp_servers.sql_tool import SQLTool
from mcp_servers.rag_tool import RAGTool

class EmployeeChatbotServer(FastMCP):
    def __init__(self):
        super().__init__(name="EmployeeChatbotServer")
        self.app = FastAPI()

        self.session_memories = {}  # {session_id: [{"role": "user/assistant", "content": text}]}

        self.sql_tool = SQLTool()
        self.rag_tool = RAGTool(sql_tool=self.sql_tool, session_memories=self.session_memories)
        self.add_tool(self.sql_tool)
        self.add_tool(self.rag_tool)

        @self.app.post("/call_tool")
        async def call_tool(request: dict):
            tool_name = request.get("tool")
            args = request.get("args", {})
            session_id = args.get("session_id", "default") 
            print(f"Received tool call: {tool_name}, session={session_id}, args={args}")

            if session_id not in self.session_memories:
                self.session_memories[session_id] = []

            tool = await self.get_tool(tool_name)
            if not tool:
                return {"output": f"Tool '{tool_name}' not found"}

            self.session_memories[session_id].append({"role": "user", "content": args.get("question", "")})

            result = await tool.run(**args)

            if isinstance(result, dict) and "answer" in result:
                self.session_memories[session_id].append({"role": "assistant", "content": result["answer"]})

            return {"output": result}
