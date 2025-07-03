import pandas as pd
import psycopg2
import openpyxl

conn = psycopg2.connect(database="new_db",
                        user="postgres",
                        password="gohome25",
                        host="localhost",
                        port=5432)

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

for _, row in df.iterrows():
    cur.execute("""
        INSERT INTO students (student_name, age, average_mark, gender, phone_number)
        VALUES (%s, %s, %s, %s, %s)
    """, (row['student name'], row['age'], row['average mark'], row['gender'], row['phone number']))

conn.commit()


with open("textfile.txt", "w", encoding="utf-8") as f:
    f.write(df.to_string())

cur.execute("DELETE FROM students WHERE average_mark IS NULL")
conn.commit()

df[['first_name', 'second_name']] = df['student name'].str.split(' ', n=1, expand=True)

cur.execute("""
    ALTER TABLE students
    ADD COLUMN first_name VARCHAR(64),
    ADD COLUMN second_name VARCHAR(64);
""")

for _, row in df.iterrows():
    cur.execute("""
        UPDATE students
        SET first_name = %s,
            second_name = %s
        WHERE student_name = %s
    """, (
        row['first_name'],
        row['second_name'],
        row['student name']
    ))

conn.commit()






