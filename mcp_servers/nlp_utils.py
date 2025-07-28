def llama_rephrase(user_question: str, sql_result: dict) -> str:
    try:
        prompt = f"""
        You are an assistant answering questions about an employee database.

        Question: {user_question}
        SQL Result: {sql_result}

        Instructions:
        - If the result contains 'columns' and 'rows', display the FULL data as a markdown table.
        - Do not summarize like "the table has 5 rows".
        - Always render every row in the table with proper headers.
        - Example format:

        | ID | Name | Department | Salary |
        |----|------|------------|--------|
        | 1  | Alice | HR | 70000 |
        | 2  | Bob   | IT | 80000 |
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
            data = response.json()
            return data["choices"][0]["message"]["content"].strip()

        return f"⚠️ API Error: {response.text}"
    except Exception as e:
        return f"⚠️ Request failed: {e}"
