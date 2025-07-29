import os
import requests
import json

TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

def llama_generate_sql(user_question: str, memory: list) -> str:
    try:
        prompt = f"""
        You are a SQL expert for an employee database.

        The database has a table called 'employees' with columns:
        id (integer), name (text), department (text), salary (integer).

        Use the following recent conversation for context:
        {json.dumps(memory[-3:], indent=2) if memory else "No prior context."}

        Task:
        - Convert the user's question into a valid SQL SELECT query.
        - Only output the SQL query, nothing else.
        - Ensure the query is safe (no UPDATE, DELETE, INSERT, DROP).
        - Example formats:
            SELECT COUNT(name) FROM employees;
            SELECT name FROM employees WHERE name LIKE '%e%';
            SELECT department, AVG(salary) FROM employees GROUP BY department;

        User question: {user_question}
        """

        response = requests.post(
            "https://api.together.xyz/v1/chat/completions",
            headers={"Authorization": f"Bearer {TOGETHER_API_KEY}"},
            json={
                "model": "meta-llama/Meta-Llama-3-70B-Instruct-Turbo",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 200,
            },
            timeout=30,
        )

        if response.status_code == 200:
            data = response.json()
            sql_query = data["choices"][0]["message"]["content"].strip()
            sql_query = sql_query.split("```sql")[-1].split("```")[0].strip()
            return sql_query

        return "SELECT * FROM employees;"  # fallback safe query

    except Exception as e:
        return f"SELECT * FROM employees; -- fallback due to error: {e}"

def llama_rephrase(user_question: str, sql_result: dict, memory: list) -> str:
    try:
        prompt = f"""
        You are a helpful assistant answering questions about an employee database.

        Question: {user_question}
        SQL Result: {json.dumps(sql_result, indent=2)}

        Conversation so far:
        {json.dumps(memory[-3:], indent=2) if memory else "No prior context."}

        Please provide a clear, natural, and user-friendly response in full sentences.
        If the result is a list or table, describe it neatly.
        """

        response = requests.post(
            "https://api.together.xyz/v1/chat/completions",
            headers={"Authorization": f"Bearer {TOGETHER_API_KEY}"},
            json={
                "model": "meta-llama/Meta-Llama-3-70B-Instruct-Turbo",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 300,
            },
            timeout=30,
        )

        if response.status_code == 200:
            data = response.json()
            return data["choices"][0]["message"]["content"].strip()

        return "Sorry, I couldn’t generate a response."
    except Exception as e:
        return f"Error during rephrasing: {e}"
