import discord
from database.db import get_connection

def upsert_guild(guild: discord.Guild):
    conn = get_connection()
    cursor = conn.cursor()

    guild_id = str(guild.id)
    guild_name = guild.name
    created_at = guild.created_at.isoformat()

    cursor.execute("""
        INSERT INTO guilds (guild_id, guild_name, created_at)
            VALUES (?, ?, ?)
            ON CONFLICT(guild_id) DO UPDATE SET
                guild_name = EXCLUDED.guild_name,
                created_at = EXCLUDED.created_at
                   """, (guild_id, guild_name, created_at))
    
    conn.commit()
    conn.close()