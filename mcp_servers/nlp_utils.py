import os
import requests
import json

TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

def llama_generate_sql(question: str) -> str:
    try:
        prompt = f"""
        You are an expert SQL assistant.
        Convert the following natural language question into a SQL SELECT query.
        The table name is employees, and columns are id, name, department, and salary.
        
        Question: {question}
        
        Only return the SQL query. Do not include explanations.
        Ensure the query is safe and uses only SELECT.
        """

        response = requests.post(
            "https://api.together.xyz/v1/chat/completions",
            headers={"Authorization": f"Bearer {TOGETHER_API_KEY}"},
            json={
                "model": "meta-llama/Meta-Llama-3-70B-Instruct-Turbo",
                "messages": [{"role": "user", "content": prompt}],
            },
            timeout=30,
        )

        if response.status_code == 200:
            sql = response.json()["choices"][0]["message"]["content"].strip()
            return sql if sql.lower().startswith("select") else "SELECT * FROM employees;"
        return "SELECT * FROM employees;"
    except:
        return "SELECT * FROM employees;"

def llama_rephrase(user_question: str, sql_result: dict) -> str:
    try:
        prompt = f"""
        You are an assistant answering questions about an employee database.

        Question: {user_question}
        SQL Result (JSON): {json.dumps(sql_result)}

        Instructions:
        - If the result is a count, answer directly like: "There are 5 employees."
        - If the result is a list of names, list them naturally.
        - If the result is a full table (with multiple columns), format it nicely in text:
          Example: "Here are the employees:\n1. Alice - HR - $70,000\n2. Bob - IT - $80,000"
        - Do NOT just summarize vaguely. Use the actual rows.
        - Respond in natural, conversational English.
        """

        response = requests.post(
            "https://api.together.xyz/v1/chat/completions",
            headers={"Authorization": f"Bearer {TOGETHER_API_KEY}"},
            json={
                "model": "meta-llama/Meta-Llama-3-70B-Instruct-Turbo",
                "messages": [{"role": "user", "content": prompt}],
            },
            timeout=40,
        )

        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"].strip()

        return f"API Error: {response.text}"
    except Exception as e:
        return f"Request failed: {e}"
