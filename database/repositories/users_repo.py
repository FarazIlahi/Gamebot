from database.db import get_connection


def upsert_user(member):
    conn = get_connection()
    cursor = conn.cursor()

    user_id = str(member.id)
    username = member.name
    display_name = member.display_name
    pfp_url = str(member.avatar.url) if member.avatar else None

    cursor.execute("""
        INSERT INTO users (user_id, username, display_name, pfp_url)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            username = excluded.username,
            display_name = excluded.display_name,
            pfp_url = excluded.pfp_url
    """, (user_id, username, display_name, pfp_url))

    conn.commit()
    conn.close()

def get_all_users():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
                   SELECT display_name 
                   FROM users
                   ORDER BY LOWER(display_name) ASC
                   """)
    rows = cursor.fetchall()
    names = [row[0] for row in rows]
    conn.close()
    return "\n".join(names)
    

