import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()  # Load environment variables from .env

def main():
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3307")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
    )
    print("Connected to MySQL:", conn.get_server_info())
    conn.close()

if __name__ == "__main__":
    main()
