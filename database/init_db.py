from db import get_connection
from schema import USERS_TABLE, ROLES_TABLE, GUILDS_TABLE

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(USERS_TABLE)
    cursor.execute(GUILDS_TABLE)
    cursor.execute(ROLES_TABLE)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()