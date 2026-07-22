import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    os.getenv("DATABASE_URL")
)

cursor = conn.cursor()

cursor.execute("SELECT current_database();")

resultado = cursor.fetchone()

print("Banco conectado:", resultado[0])

cursor.close()
conn.close()