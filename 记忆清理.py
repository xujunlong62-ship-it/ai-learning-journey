import sqlite3

path = r"D:\SystemData\Python\damoxing\对话记忆\checkpoint.db"
conn = sqlite3.connect(path)
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [row[0] for row in cursor.fetchall()]

for table in tables:
    cursor.execute(f"DELETE FROM {table}")
    print("已清空表：", table)

conn.commit()
conn.close()