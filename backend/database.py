import sqlite3
import json

DB_FILE = "storage.db"


def init_db():
    """
    Initializes the SQLite database, creates the required table,
    and clears old data on server restart.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Create table if not exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS graphql_links (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            link TEXT UNIQUE NOT NULL,
            schema TEXT NOT NULL
        )
    """)

    # ✅ Clear the table on startup
    cursor.execute("DELETE FROM graphql_links")
    conn.commit()

    conn.close()
    print("[DEBUG] Database initialized and cleared on startup.")


def store_graphql_link_and_schema(link, schema):
    """
    Stores or updates the GraphQL link and schema in the database.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Convert schema (dict) to a JSON string for storage
    schema_json = json.dumps(schema)

    # Check if a link already exists
    cursor.execute("SELECT link FROM graphql_links")
    existing_link = cursor.fetchone()

    if existing_link:
        # Update the existing link and schema
        cursor.execute("UPDATE graphql_links SET link = ?, schema = ? WHERE id = 1", (link, schema_json))
    else:
        # Insert new link and schema
        cursor.execute("INSERT INTO graphql_links (id, link, schema) VALUES (1, ?, ?)", (link, schema_json))

    conn.commit()
    conn.close()
    print(f"[DEBUG] Stored GraphQL link: {link} with schema.")


def get_stored_graphql_link_and_schema():
    """
    Retrieves the stored GraphQL link and schema from the database.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT link, schema FROM graphql_links LIMIT 1")
    row = cursor.fetchone()

    conn.close()
    if row:
        link, schema_json = row
        return link, json.loads(schema_json)  # Convert JSON back to dict
    return None, None  # Return None if no data found
