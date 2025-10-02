"""
Script pour forcer la synchronisation Redis au démarrage
"""

import os
import sys
import time

import mysql.connector

from db import get_mysql_conn, get_redis_conn
from stocks.commands.write_stock import _populate_redis_from_mysql


def check_db_connection():
    """Check DB connection with 5 retries"""
    for i in range(5):
        try:
            mysql_conn = get_mysql_conn()
            mysql_conn.ping()
            mysql_conn.close()

            redis_conn = get_redis_conn()
            redis_conn.ping()
            return True
        except Exception as e:
            print(f"DB check {i+1}/5 failed: {e}")
            if i < 4:
                time.sleep(2)
    return False


def sync_redis_with_mysql():
    """Force la synchronisation complète de Redis avec MySQL"""
    if not check_db_connection():
        print("DB connection failed")
        sys.exit(1)

    try:
        r = get_redis_conn()
        r.flushdb()
        _populate_redis_from_mysql(r)
        print("Redis sync done")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
        print(f"Error: {e}")
        sys.exit(1)
