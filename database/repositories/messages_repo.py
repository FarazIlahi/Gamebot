from email.mime import message

import discord
from database.db import get_connection

def upsert_messages(message: discord.Message):
    conn = get_connection()
    cursor = conn.cursor()

    message_id = str(message.id)
    user_id = str(message.author.id)
    guild_id = str(message.guild.id)
    channel_id = str(message.channel.id)
    content = message.content
    created_at = message.created_at.isoformat()
    is_bot = 1 if message.author.bot else 0
    is_edited = 1 if message.edited_at else 0

    cursor.execute("""
        INSERT INTO messages (message_id, user_id, guild_id, channel_id, content, created_at, is_bot, is_edited)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(message_id) DO UPDATE SET
                content = EXCLUDED.content,
                is_edited = EXCLUDED.is_edited
                   """, (message_id, user_id, guild_id, channel_id, content, created_at, is_bot, is_edited))

    conn.commit()
    conn.close()
