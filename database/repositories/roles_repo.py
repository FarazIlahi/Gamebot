import discord
from database.db import get_connection

def upsert_role(role: discord.Role, created_by_user_id: int | None = None, is_color_role: bool = False):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO roles (role_id, guild_id, created_by_user_id, is_color_role)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(role_id) DO UPDATE SET
            guild_id = excluded.guild_id,
            created_by_user_id = COALESCE(excluded.created_by_user_id, roles.created_by_user_id),
            is_color_role = excluded.is_color_role
    """, (
        str(role.id),
        str(role.guild.id),
        str(created_by_user_id) if created_by_user_id is not None else None,
        1 if is_color_role else 0
    ))

    conn.commit()
    conn.close()

def get_all_custom_color_roles(guild_id: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
                   SELECT role_id
                   FROM roles
                   WHERE is_color_role = 1 AND guild_id = ?
                   """, (guild_id,))
    rows = cursor.fetchall()
    roles = [row[0] for row in rows]
    conn.close()
    return (roles)  

def get_all_custom_color_roles_creator(guild_id: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
                   SELECT created_by_user_id
                   FROM roles
                   WHERE is_color_role = 1 AND guild_id = ?
                   """, (guild_id,))
    rows = cursor.fetchall()
    names = [row[0] for row in rows]
    conn.close()
    return (names)  

def get_role(created_by_user_id: str, guild_id: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
                   SELECT role_id
                   FROM roles
                   WHERE is_color_role = 1 AND created_by_user_id = ? AND guild_id = ?
                   """, (created_by_user_id, guild_id))
    row = cursor.fetchone()
    conn.close()
    if row:
        return row[0]  # single value
    return None

def get_all_roles(guild_id: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
                   SELECT role_id
                   FROM roles
                   WHERE guild_id = ?
                   """, (guild_id,))
    rows = cursor.fetchall()
    roles = [row[0] for row in rows]
    conn.close()
    return (roles)
