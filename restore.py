# restore_to_postgres.py
import psycopg2, json

# PostgreSQL config
PG_HOST = "<RDS_ENDPOINT>"
PG_PORT = 5432
PG_DATABASE = "<your_database>"
PG_USER = "<your_user>"
PG_PASSWORD = "<your_password>"

# File to restore from
BACKUP_FILE = "/home/ubuntu/Redis_Backups/redis_backup.json"
TABLE_NAME = "redis_data"

# Connect to PostgreSQL
conn = psycopg2.connect(
    host=PG_HOST, port=PG_PORT, dbname=PG_DATABASE,
    user=PG_USER, password=PG_PASSWORD
)
cursor = conn.cursor()

cursor.execute(f"""
CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
    key TEXT PRIMARY KEY,
    value TEXT
)
""")
conn.commit()

with open(BACKUP_FILE, 'r') as f:
    data = json.load(f)

for key, value in data.items():
    cursor.execute(f"""
    INSERT INTO {TABLE_NAME} (key, value)
    VALUES (%s, %s)
    ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value
    """, (key, value))

conn.commit()
cursor.close()
conn.close()

print("✅ Data restored to PostgreSQL.")

