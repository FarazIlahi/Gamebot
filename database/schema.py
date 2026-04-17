USERS_TABLE = """
    CREATE TABLE IF NOT EXISTS users (
        user_id TEXT PRIMARY KEY,
        username TEXT NOT NULL,
        display_name TEXT,
        pfp_url TEXT
    )
    """

ROLES_TABLE = """
    CREATE TABLE IF NOT EXISTS roles (
        role_id TEXT PRIMARY KEY,
        guild_id TEXT,
        role_name TEXT,
        created_by_user_id TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (created_by_user_id) REFERENCES users(user_id)
    )
    """