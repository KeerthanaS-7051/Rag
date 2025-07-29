import streamlit as st
import requests

st.set_page_config(page_title="Employee Database Chatbot", page_icon="🤖")
st.title("🤖 Employee Database Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

def query_mcp(question: str):
    try:
        response = requests.post(
            "http://127.0.0.1:8000/call_tool",
            json={
                "tool": "rag_query",   
                "args": {"question": question}
            },
            timeout=30,
        )
        if response.status_code == 200:
            data = response.json()
            output = data.get("output", {})

            if isinstance(output, dict):
                return output.get("answer", "No answer found.")
            elif isinstance(output, str):
                return output
            else:
                return str(output)

        return f"Server returned {response.status_code}: {response.text}"

    except Exception as e:
        return f"Connection error: {e}"

user_input = st.chat_input("Ask a question about employees")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.spinner("Thinking..."):
        answer = query_mcp(user_input)
    st.session_state.messages.append({"role": "assistant", "content": answer})

for msg in st.session_state.messages:
    role = "user" if msg["role"] == "user" else "assistant"
    content = msg["content"]

    if "|" in content and "---" in content:  # crude check for markdown table
        st.chat_message(role).markdown(content)
    else:
        st.chat_message(role).write(content)
