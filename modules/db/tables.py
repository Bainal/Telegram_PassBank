queries = [
    """
    CREATE TABLE IF NOT EXISTS settings (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    name       TEXT    UNIQUE,
    value      TEXT    UNIQUE
);
    """
]
