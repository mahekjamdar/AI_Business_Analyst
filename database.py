import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

connection = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT")),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

cursor = connection.cursor()

cursor.execute("SELECT COUNT(*) FROM sales_data")

result = cursor.fetchone()

print("Total records:", result[0])

cursor.close()
connection.close()