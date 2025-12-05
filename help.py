import os
import sys
from datetime import datetime, timedelta, date as datetime_date
import logging
import pymysql
from dotenv import load_dotenv
import csv


# 載入 .env 檔案
load_dotenv()


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


logger = logging.getLogger()

# 設定日誌層級，預設為 INFO
log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
logger.setLevel(getattr(logging, log_level, logging.INFO))

handler = logging.StreamHandler(sys.stdout)


source_user_id = os.getenv('SOURCE_DB_USER_ID')


target_user_id = os.getenv('TARGET_DB_USER_ID')


# 設定日誌格式
class CustomFormatter(logging.Formatter):
    blue = "\x1b[34;20m"
    white = "\x1b[37;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    reset = "\x1b[0m"
    format_str = "%(asctime)s - %(levelname)s - %(message)s"

    FORMATS = {
        logging.DEBUG: blue + format_str + reset,
        logging.INFO: white + format_str + reset,
        logging.WARNING: yellow + format_str + reset,
        logging.ERROR: red + format_str + reset,
        logging.CRITICAL: red + format_str + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno, self.white + self.format_str + self.reset)
        formatter = logging.Formatter(log_fmt, datefmt='%Y-%m-%d %H:%M:%S')
        return formatter.format(record)


handler.setFormatter(CustomFormatter())

logger.addHandler(handler)


def get_custom_week_number(date, start_weekday=6):
    """
    計算自訂週數
    start_weekday: 0=Monday, 6=Sunday (預設為Sunday)
    """
    # 找到該年的第一個指定星期幾
    first_day_of_year = datetime_date(date.year, 1, 1)
    # 計算第一個指定星期幾是哪一天
    days_to_first_target_day = (start_weekday - first_day_of_year.weekday()) % 7  # weekday: 0=Mon, 6=Sun
    first_target_day = first_day_of_year + timedelta(days=days_to_first_target_day)
    
    # 計算從第一個指定星期幾到當前日期的天數
    days_since_first_target_day = (date - first_target_day).days
    
    # 週數 = 天數 // 7 + 1
    if days_since_first_target_day >= 0:
        week_num = (days_since_first_target_day // 7) + 1
    else:
        # 如果日期在第一個指定星期幾前，使用上一年的週數（這裡簡化，實際可能需要調整）
        week_num = 52  # 或計算上一年
    
    return week_num

# 定義 user_id 的置換對應表
USER_ID_MAPPING = {
    6: 60,
    10: 30,
    13: 17,
    17: 13,
    21: 5,
    22: 32,
    54: 38,
    73: 69,
    85: 66,
    127: 65,
    306: 53,
    580: 164,
    1478: 498,
    1069: 61,
    2793: 490,
    3283: 492,
    7351: 1238,
    9567: 1239,
    14755: 1218
}


def fetch_data(src_config, select_sql):
    """
    取得來源資料庫的資料
    """
    conn = pymysql.connect(**src_config)
    try:
        with conn.cursor() as cursor:
            cursor.execute(select_sql)
            columns = [desc[0] for desc in cursor.description]
            results = cursor.fetchall()
            return columns, results
    finally:
        conn.close()


def get_now():
    """
    取得當前時間，若有設定環境變數 TEST_DATE 則使用該時間
    TEST_DATE 格式: YYYY-MM-DD 或 YYYY-MM-DD HH:MM:SS
    """
    test_date = os.getenv('TEST_DATE')
    if test_date:
        try:
            # 嘗試解析包含時間的格式
            return datetime.strptime(test_date, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            try:
                # 嘗試解析只包含日期的格式
                return datetime.strptime(test_date, "%Y-%m-%d")
            except ValueError:
                logger.warning(f"TEST_DATE 格式錯誤: {test_date}，將使用系統時間。")
    return datetime.now()


def save_to_csv(columns, data, filename="output.csv"):
    """
    將資料寫入 CSV 檔案
    """
    try:
        # 使用 utf-8-sig 編碼以支援 Excel 開啟中文
        with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(columns)
            writer.writerows(data)
        logger.debug(f"資料已成功寫入 {filename} 共 {len(data)} 筆資料至 csv 檔")
    except Exception as e:
        logger.error(f"寫入 CSV 失敗: {e}")


def convert_user_id(columns, data):
    """
    將 user_id 轉換為對應的值
    """
    new_data = []
    for row in data:
        row_list = list(row)
        original_uid = row_list[columns.index('user_id')]
        if original_uid in USER_ID_MAPPING:
            row_list[columns.index('user_id')] = USER_ID_MAPPING[original_uid]
        new_data.append(tuple(row_list))
    return new_data


def save_to_csv_with_user_id_mapping(columns, data, filename="output.csv"):
    """
    將資料寫入 CSV 檔案(已轉換過 user_id)
    """

    # 檢查是否有 user_id 欄位，若有則進行轉換 rows
    if 'user_id' in columns:
        user_id_idx = columns.index('user_id')
        new_rows = []
        for row in data:
            row_list = list(row)
            original_uid = row_list[user_id_idx]
            if original_uid in USER_ID_MAPPING:
                row_list[user_id_idx] = USER_ID_MAPPING[original_uid]
            new_rows.append(tuple(row_list))
        
        # 檢查轉換後是否有重複資料 (僅供除錯提示)
        if len(new_rows) != len(set(new_rows)):
            logger.warning(f"注意: 資料表在 user_id 轉換後發現重複資料，這可能導致 INSERT IGNORE 寫入筆數減少。")

    try:
        # 使用 utf-8-sig 編碼以支援 Excel 開啟中文
        with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(columns)
            writer.writerows(new_rows)
        logger.debug(f"資料已成功寫入(已轉換過 user_id) {filename} 共 {len(new_rows)} 筆資料至 csv 檔")
    except Exception as e:
        logger.error(f"寫入 CSV 失敗: {e}")


def check_db_connection(script_name):
    """
    檢查資料庫連線
    """
    try:
        conn = pymysql.connect(**source_config)
        with conn.cursor() as cursor:
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()

            # log 要記錄今天執行是日期
            today_str = get_now().strftime("%Y-%m-%d")
            logger.debug(f"========================================================")
            logger.debug(f"執行日期: {today_str}")    
            logger.debug(f"執行腳本: {script_name}.py")    
            logger.debug(f"========================================================")
            logger.debug(f"來源資料庫: {source_config['host']} 資料庫連線成功！版本: {version[0]}")
            logger.debug(f"目標資料庫: {target_config['host']}")
            logger.debug(f"========================================================")
        conn.close()
        return True
    except Exception as e:
        logger.error(f"{source_config['host']} 資料庫連線失敗: {e}")
        return False


def delete_day_data(table_name, current_year, today_str, current_week_mon, current_week_sun, current_day_mon, current_day_sun):
    """
    刪除 day 資料 (針對目標資料庫)
    """
    sql = ""
    sql_online = ""
    if table_name == "activity_day":
        sql = f"DELETE FROM activity_day WHERE year_num = {current_year} AND start_time >= '{today_str}T00:00:00.000+08:00' AND start_time <= '{today_str}T23:59:59.999+08:00';"
        sql_online = f"DELETE FROM activity_day_online WHERE year_num = {current_year} AND start_time >= '{today_str}T00:00:00.000+08:00' AND start_time <= '{today_str}T23:59:59.999+08:00';"
    elif table_name == "activity_day_of_first_monday":
        sql = f"DELETE FROM activity_day_of_first_monday WHERE year_num = {current_year} AND start_time >= '{today_str}T00:00:00.000+08:00' AND start_time <= '{today_str}T23:59:59.999+08:00';"
        sql_online = f"DELETE FROM activity_day_of_first_monday_online WHERE year_num = {current_year} AND start_time >= '{today_str}T00:00:00.000+08:00' AND start_time <= '{today_str}T23:59:59.999+08:00';"
    elif table_name == "activity_day_weight_training":
        sql = f"DELETE FROM activity_day_weight_training WHERE year_num = {current_year} AND week_num = {current_week_sun} AND day_num = {current_day_sun};"
        sql_online = f"DELETE FROM activity_day_weight_training_online WHERE year_num = {current_year} AND week_num = {current_week_sun} AND day_num = {current_day_sun};"
    elif table_name == "activity_day_weight_training_of_first_monday":
        sql = f"DELETE FROM activity_day_weight_training_of_first_monday WHERE year_num = {current_year} AND week_num = {current_week_mon} AND day_num = {current_day_mon};"
        sql_online = f"DELETE FROM activity_day_weight_training_of_first_monday_online WHERE year_num = {current_year} AND week_num = {current_week_mon} AND day_num = {current_day_mon};"

    conn = pymysql.connect(**target_config)
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            cursor.execute(sql_online)
        conn.commit()
        logger.debug(f"目標資料庫: {target_config['host']}，{table_name} SQL 指令執行成功")
    except Exception as e:
        logger.error(f"目標資料庫: {target_config['host']}，{table_name} SQL 指令執行失敗: {e}")
        raise e
    finally:
        conn.close()


def execute_sql(sql):
    """
    執行 SQL 指令 (針對目標資料庫)
    """
    conn = pymysql.connect(**target_config)
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql)
        conn.commit()
        logger.debug(f"目標資料庫: {target_config['host']}，SQL 指令執行成功")
    except Exception as e:
        logger.error(f"目標資料庫: {target_config['host']}，SQL 指令執行失敗: {e}")
        raise e
    finally:
        conn.close()


def insert_data(table_name, columns, rows):
    """
    將資料寫入目標資料庫
    """

    # 檢查是否有 user_id 欄位，若有則進行轉換
    if 'user_id' in columns:
        user_id_idx = columns.index('user_id')
        new_rows = []
        for row in rows:
            row_list = list(row)
            original_uid = row_list[user_id_idx]
            if original_uid in USER_ID_MAPPING:
                row_list[user_id_idx] = USER_ID_MAPPING[original_uid]
            new_rows.append(tuple(row_list))
        
        # 檢查轉換後是否有重複資料 (僅供除錯提示)
        if len(new_rows) != len(set(new_rows)):
            logger.warning(f"注意: 資料表 {table_name} 在 user_id 轉換後發現重複資料，這可能導致 INSERT IGNORE 寫入筆數減少。")

        rows = new_rows

    conn = pymysql.connect(**target_config)
    try:
        with conn.cursor() as cursor:
            # 動態產生 INSERT SQL 指令
            # 格式: INSERT IGNORE INTO table_name (col1, col2, ...) VALUES (%s, %s, ...)
            # 使用 backticks (`) 包裹欄位名稱以避免關鍵字衝突
            cols_str = ", ".join([f"`{col}`" for col in columns])
            placeholders = ", ".join(["%s"] * len(columns))
            insert_sql = f"INSERT IGNORE INTO `{table_name}` ({cols_str}) VALUES ({placeholders})"
            
            # 執行批次寫入
            cursor.executemany(insert_sql, rows)
            
            # 取得實際影響的筆數 (INSERT IGNORE 成功寫入會回傳 1，重複忽略回傳 0)
            affected_rows = cursor.rowcount
            ignored_count = len(rows) - affected_rows

            if ignored_count > 0:
                logger.warning(f"資料表 {table_name}: 共有 {ignored_count} 筆資料被忽略 (可能是重複鍵值或其他原因)")
                # 查看警告訊息以了解原因
                cursor.execute("SHOW WARNINGS")
                warnings = cursor.fetchall()
                # 為了避免 log 太多，只顯示前 5 筆警告
                for i, w in enumerate(warnings[:5]):
                    # w 的格式通常是 (Level, Code, Message)
                    logger.warning(f"  警告詳情 ({i+1}): {w[2]}")
                if len(warnings) > 5:
                    logger.warning(f"  ... 還有 {len(warnings) - 5} 筆警告未顯示")

        conn.commit()
        if len(rows) != affected_rows:
            logger.warning(f"目標資料庫: {target_config['host']}，資料表 {table_name}: 預計寫入 {len(rows)} 筆, 成功 {affected_rows} 筆, 忽略 {ignored_count} 筆")
        else:
            logger.info(f"目標資料庫: {target_config['host']}，資料表 {table_name}: 預計寫入 {len(rows)} 筆, 成功 {affected_rows} 筆, 忽略 {ignored_count} 筆")
    except Exception as e:
        logger.error(f"寫入資料庫失敗: {e}")
    finally:
        conn.close()


def compare_data(source_data_with_user_id_mapping, target_data):
    """
    比對來源資料和目標資料
    """

    diff = []
    # 檢查來源資料和目標資料的長度是否相同
    if len(source_data_with_user_id_mapping) != len(target_data):
        logger.warning(f"來源資料和目標資料的長度不同，來源資料有 {len(source_data_with_user_id_mapping)} 筆，目標資料有 {len(target_data)} 筆")
    else:
        return diff

    # 檢查來源資料和目標資料的內容是否相同
    for i in range(len(source_data_with_user_id_mapping)):
        # 檢查 source_data_with_user_id_mapping[i] 是否存在於 target_data 中
        if source_data_with_user_id_mapping[i] not in target_data:
            logger.warning(f"來源資料和目標資料的內容不同，目標缺少 user_id {source_data_with_user_id_mapping[i][0]} 且 type 為 {source_data_with_user_id_mapping[i][5]}")
            diff.append(source_data_with_user_id_mapping[i])
    return diff

