import redis
import json
import os
from datetime import datetime
# === Upstash Redis Credentials ===
UPSTASH_HOST = "pumped-imp-47806.upstash.io"
UPSTASH_PORT = 6379
UPSTASH_PASSWORD = "<your_password>"  # Replace with your actual password
# === Backup Directory ===
BACKUP_DIR = "/home/ubuntu/Redis_Backups"
os.makedirs(BACKUP_DIR, exist_ok=True)
TIMESTAMP = datetime.now().strftime('%Y%m%d_%H%M%S')
BACKUP_FILE = os.path.join(BACKUP_DIR, f"redis_backup_{TIMESTAMP}.json")
# === Connect to Redis ===
client = redis.Redis(
    host=UPSTASH_HOST,
    port=UPSTASH_PORT,
    password=UPSTASH_PASSWORD,
    ssl=True
)
def backup_redis():
    try:
        keys = client.keys('*')
        backup_data = {}
        for key in keys:
            key_str = key.decode()
            value = client.get(key)
            backup_data[key_str] = value.decode() if value else None
        with open(BACKUP_FILE, 'w') as f:
            json.dump(backup_data, f, indent=2)
        print(f":white_check_mark: Redis backup successful! File saved: {BACKUP_FILE}")
    except Exception as e:
        print(f":x: Redis backup failed: {str(e)}")
if __name__ == "__main__":
    backup_redis()