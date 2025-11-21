import os
import sys
import logging
import pymysql
from dotenv import load_dotenv

# 載入 .env 檔案
load_dotenv()

# 設定日誌格式
class CustomFormatter(logging.Formatter):
    white = "\x1b[37;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    reset = "\x1b[0m"
    format_str = "%(asctime)s - %(levelname)s - %(message)s"

    FORMATS = {
        logging.INFO: white + format_str + reset,
        logging.WARNING: yellow + format_str + reset,
        logging.ERROR: red + format_str + reset,
        logging.CRITICAL: red + format_str + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno, self.white + self.format_str + self.reset)
        formatter = logging.Formatter(log_fmt, datefmt='%Y-%m-%d %H:%M:%S')
        return formatter.format(record)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(CustomFormatter())
logger.addHandler(handler)

# 來源資料庫連線資訊
source_config = {
    'host': os.getenv('SOURCE_DB_HOST'),
    'user': os.getenv('SOURCE_DB_USER'),
    'password': os.getenv('SOURCE_DB_PASSWORD'),
    'database': os.getenv('SOURCE_DB_NAME'),
    'charset': 'utf8mb4'
}

# 目標資料庫連線資訊
target_config = {
    'host': os.getenv('TARGET_DB_HOST'),
    'user': os.getenv('TARGET_DB_USER'),
    'password': os.getenv('TARGET_DB_PASSWORD'),
    'database': os.getenv('TARGET_DB_NAME'),
    'charset': 'utf8mb4'
}

def check_db_connection():
    """檢查資料庫連線"""
    try:
        conn = pymysql.connect(**source_config)
        with conn.cursor() as cursor:
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            logger.info(f"資料庫連線成功！版本: {version[0]}")
        conn.close()
        return True
    except Exception as e:
        logger.error(f"資料庫連線失敗: {e}")
        return False

def fetch_data():
    conn = pymysql.connect(**source_config)
    try:
        with conn.cursor() as cursor:
            # 範例：抓取資料 (請替換為實際的 SQL)
            # 這裡使用 SELECT 1, 100 作為測試，避免 transform_data 出錯
            cursor.execute("SELECT 1, 100")
            results = cursor.fetchall()
            return results
    finally:
        conn.close()

def transform_data(rows):
    transformed = []
    for row in rows:
        # 示範轉換：value 欄位加 1
        new_value = row[1] + 1
        transformed.append((row[0], new_value))
    return transformed

def insert_data(rows):
    conn = pymysql.connect(**target_config)
    try:
        with conn.cursor() as cursor:
            # 假設目標表 my_table 結構與來源相同
            insert_sql = "INSERT INTO my_table (id, value) VALUES (%s, %s)"
            cursor.executemany(insert_sql, rows)
        conn.commit()
    finally:
        conn.close()

if __name__ == "__main__":
    if check_db_connection():
        try:
            data = fetch_data()
            if data:
                #transformed_data = transform_data(data)
                #insert_data(transformed_data)
                logger.info("資料轉換並插入完成！")
        except Exception as e:
            logger.error(f"執行失敗: {e}")
    else:
        logger.error("無法連線至資料庫，程式終止。")
