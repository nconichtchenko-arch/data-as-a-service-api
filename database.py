import os
import psycopg2
from psycopg2.extras import RealDictCursor

# Читаем настройки из переменных окружения (с фолбэком на локальные)
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 5432)),
    "dbname": os.getenv("DB_NAME", "dwh_marketplace"),
    "user": os.getenv("DB_USER", "dwh_user"),
    "password": os.getenv("DB_PASSWORD", "dwh_password"),
}

def get_db_connection():
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    return conn, cursor