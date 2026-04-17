USERS_TABLE = """
    CREATE TABLE IF NOT EXISTS users (
        user_id TEXT PRIMARY KEY,
        username TEXT NOT NULL,
        display_name TEXT,
        pfp_url TEXT
    )
    """

ROLES_TABLE = """
    CREATE TABLE roles (
        role_id TEXT PRIMARY KEY,
        guild_id TEXT NOT NULL,
        created_by_user_id TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        is_color_role INTEGER DEFAULT 0,
        FOREIGN KEY (guild_id) REFERENCES guilds(guild_id),
        FOREIGN KEY (created_by_user_id) REFERENCES users(user_id)
    )
    """

GUILDS_TABLE = """
    CREATE TABLE guilds (
        guild_id TEXT PRIMARY KEY,
        guild_name TEXT NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """
