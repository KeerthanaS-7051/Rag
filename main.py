import uvicorn
from mcp_servers.server import EmployeeChatbotServer

def main():
    server = EmployeeChatbotServer()
    print("Employee Chatbot MCP Server running on HTTP...")
    uvicorn.run(server.app, host="127.0.0.1", port=8000)

if __name__ == "__main__":
    main()
