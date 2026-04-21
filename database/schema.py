USERS_TABLE = """
    CREATE TABLE IF NOT EXISTS users (
        user_id TEXT PRIMARY KEY,
        username TEXT NOT NULL,
        display_name TEXT,
        pfp_url TEXT
    )
    """
GUILDS_TABLE = """
    CREATE TABLE IF NOT EXISTS guilds (
        guild_id TEXT PRIMARY KEY,
        guild_name TEXT NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """

ROLES_TABLE = """
    CREATE TABLE IF NOT EXISTS roles (
        role_id TEXT PRIMARY KEY,
        guild_id TEXT NOT NULL,
        created_by_user_id TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        is_color_role INTEGER DEFAULT 0,
        FOREIGN KEY (guild_id) REFERENCES guilds(guild_id),
        FOREIGN KEY (created_by_user_id) REFERENCES users(user_id)
    )
    """

MESSAGES_TABLE = """
    CREATE TABLE IF NOT EXISTS messages (
    message_id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    guild_id TEXT NOT NULL,
    channel_id TEXT NOT NULL,
    content TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    is_bot INTEGER DEFAULT 0,
    is_edited INTEGER DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (guild_id) REFERENCES guilds(guild_id)
);
    """
EDITED_MESSAGES_TABLE = """
    CREATE TABLE IF NOT EXISTS message_edits  (
        edit_id TEXT PRIMARY KEY,
        message_id TEXT NOT NULL,
        old_content TEXT,
        edited_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (message_id) REFERENCES messages(message_id)
    );
    """
