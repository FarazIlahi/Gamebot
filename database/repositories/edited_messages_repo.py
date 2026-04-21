from email.mime import message

import discord
from database.db import get_connection

def insert_edited_messages(before: discord.Message, after: discord.Message):
    conn = get_connection()
    cursor = conn.cursor()
    
    edit_id = str(after.id) + "_" + after.edited_at.isoformat()
    message_id = str(after.id)
    old_content = before.content
    edited_at = after.edited_at.isoformat()

    cursor.execute("""
        INSERT INTO message_edits (edit_id, message_id, old_content, edited_at)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(message_id) DO UPDATE SET
                content = EXCLUDED.content,
                is_edited = EXCLUDED.is_edited
                   """, (edit_id, message_id, old_content, edited_at))

    conn.commit()
    conn.close()
