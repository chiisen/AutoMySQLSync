import os
import sys
import csv
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

def fetch_data(table_name):
    conn = pymysql.connect(**source_config)
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT * FROM alatech.{table_name} LIMIT 10;")
            columns = [desc[0] for desc in cursor.description]
            results = cursor.fetchall()
            return columns, results
    finally:
        conn.close()

def transform_data(rows):
    transformed = []
    for row in rows:
        # 示範轉換：value 欄位加 1
        new_value = row[1] + 1
        transformed.append((row[0], new_value))
    return transformed

def insert_data(table_name, columns, rows):
    conn = pymysql.connect(**target_config)
    try:
        with conn.cursor() as cursor:
            # 動態產生 INSERT SQL 指令
            # 格式: INSERT INTO table_name (col1, col2, ...) VALUES (%s, %s, ...)
            # 使用 backticks (`) 包裹欄位名稱以避免關鍵字衝突
            cols_str = ", ".join([f"`{col}`" for col in columns])
            placeholders = ", ".join(["%s"] * len(columns))
            insert_sql = f"INSERT INTO `{table_name}` ({cols_str}) VALUES ({placeholders})"
            
            # 執行批次寫入
            cursor.executemany(insert_sql, rows)
        conn.commit()
        logger.info(f"成功寫入 {len(rows)} 筆資料至目標資料庫的 {table_name} 資料表")
    except Exception as e:
        logger.error(f"寫入資料庫失敗: {e}")
    finally:
        conn.close()

def save_to_csv(columns, data, filename="output.csv"):
    """將資料寫入 CSV 檔案"""
    try:
        # 使用 utf-8-sig 編碼以支援 Excel 開啟中文
        with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(columns)
            writer.writerows(data)
        logger.info(f"資料已成功寫入 {filename}")
    except Exception as e:
        logger.error(f"寫入 CSV 失敗: {e}")

if __name__ == "__main__":
    if check_db_connection():
        # 定義要匯出的資料表清單
        table_names = [
            "activity_day",
            # "other_table_name", # 在此添加更多資料表
        ]
        
        # 確保 csv 目錄存在
        dirs = "output"
        os.makedirs(f"./{dirs}", exist_ok=True)

        for table_name in table_names:
            try:
                logger.info(f"正在處理資料表: {table_name}")
                columns, data = fetch_data(table_name)
                if data:
                    save_to_csv(columns, data, f"./{dirs}/{table_name}.csv")
                    
                    # 同步寫入目標資料庫
                    insert_data(f"{table_name}_backup", columns, data)
                else:
                    logger.warning(f"資料表 {table_name} 無資料")
            except Exception as e:
                logger.error(f"處理資料表 {table_name} 時發生錯誤: {e}")
    else:
        logger.error("無法連線至資料庫，程式終止。")
