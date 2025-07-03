import pandas as pd
import psycopg2

conn = psycopg2.connect(database="python_practice", user="katet",
    password="gohome25", host="localhost", port=5432)

df = pd.read_excel("students.xlsx")

df['phone number'] = df['phone number'].apply(
    lambda x: str(int(float(x))) if pd.notna(x) else ''
)

cur = conn.cursor()
cur.execute("""
    CREATE TABLE students (
        id SERIAL PRIMARY KEY,
        student_name VARCHAR(64),
        age INT,
        average_mark FLOAT,
        gender CHAR(1),
        phone_number VARCHAR(64)
    );
""")


