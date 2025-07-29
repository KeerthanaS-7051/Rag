import sqlite3

conn = sqlite3.connect("employees.db")
c = conn.cursor()

c.execute("DROP TABLE IF EXISTS employees")
c.execute("""
CREATE TABLE employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    department TEXT,
    salary INTEGER
)
""")

c.executemany("""
INSERT INTO employees (name, department, salary)
VALUES (?, ?, ?)
""", [
    ("Alice", "HR", 70000),
    ("Bob", "Engineering", 90000),
    ("Charlie", "Finance", 85000),
    ("David", "Engineering", 95000),
    ("Eva", "Marketing", 60000)
])

conn.commit()
conn.close()
print("Employee database created.")
