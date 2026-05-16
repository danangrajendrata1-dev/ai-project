from database.db_connect import conn, cursor

cursor.execute("""
CREATE TABLE IF NOT EXISTS chats (
    id SERIAL PRIMARY KEY,
    role VARCHAR(50),
    message TEXT
)
""")

conn.commit()

print("Table chats berhasil dibuat")