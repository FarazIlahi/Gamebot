from database.db import get_connection


conn = get_connection()
cursor = conn.cursor()

cursor.execute("""
                SELECT * FROM messages
                """)

rows = cursor.fetchall()
roles = [row[0] for row in rows]
conn.close()
print(roles)
