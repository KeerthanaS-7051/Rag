import streamlit as st 
import requests
import uuid

st.set_page_config(page_title="Employee Database Chatbot", page_icon="🤖")
st.title("🤖 Employee Database Chatbot")

if "session_id" not in st.session_state:
    with st.form("session_form"):
        session_id_input = st.text_input("Enter your Session ID (leave blank to create a new one):")
        submitted = st.form_submit_button("Start Session")
        if submitted:
            if session_id_input.strip():
                st.session_state.session_id = session_id_input.strip()
            else:
                st.session_state.session_id = str(uuid.uuid4())
            st.session_state.messages = []
            st.success(f"Your session ID: {st.session_state.session_id}")

if "session_id" in st.session_state:
    def query_mcp(question: str):
        try:
            response = requests.post(
                "http://127.0.0.1:8000/call_tool",
                json={
                "tool": "rag_query",
                "args": {
                    "question": question,
                    "session_id": st.session_state.session_id
                    }
                },
                timeout=30,
            )
            if response.status_code == 200:
                data = response.json()
                output = data.get("output")
                st.write("DEBUG OUTPUT:", output) 

                if isinstance(output, dict):
                    return output.get("answer", "No answer found.")
                elif isinstance(output, str):
                    return output
                else:
                    return "Unexpected response format."

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
        st.chat_message(msg["role"]).write(msg["content"])
