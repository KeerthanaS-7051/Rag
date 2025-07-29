from fastapi import FastAPI
from fastmcp import FastMCP
from mcp_servers.sql_tool import SQLTool
from mcp_servers.rag_tool import RAGTool

class EmployeeChatbotServer(FastMCP):
    def __init__(self):
        super().__init__(name="EmployeeChatbotServer")
        self.app = FastAPI()

        self.sql_tool = SQLTool()
        self.rag_tool = RAGTool(self.sql_tool)  

        self.add_tool(self.sql_tool)
        self.add_tool(self.rag_tool)

        @self.app.post("/call_tool")
        async def call_tool(request: dict):
            tool_name = request.get("tool")
            args = request.get("args", {})

            print(f"Received call for tool={tool_name}, args={args}")

            tool = await self.get_tool(tool_name)
            if not tool:
                return {"output": f"Tool '{tool_name}' not found"}

            try:
                if callable(getattr(tool, "run", None)):
                    result = await tool.run(**args)
                    return {"output": result}
                else:
                    return {"output": f"Tool '{tool_name}' has no run()"}
            except Exception as e:
                print("Tool error:", e)
                return {"output": f"Server error: {e}"}
