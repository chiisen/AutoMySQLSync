import os
import sys
import csv
import pymysql
import time
from datetime import datetime, timedelta, date as datetime_date
from help import (
    get_custom_week_number,
    USER_ID_MAPPING,
    CustomFormatter,
    fetch_data,
    source_config,
    target_config,
    get_now,
    save_to_csv,
    save_to_csv_with_user_id_mapping,
    logger,
    source_user_id,
    target_user_id,
    check_db_connection,
    execute_sql,
    insert_data,
)

script_name = "auto_point"




if __name__ == "__main__":
    if check_db_connection(script_name):
        table_names = []
        table_select_sqls = []

        # 讀出 ./sql/point 目錄下的 SQL 指令  
        sql_dir = "./sql/point"
        sql_files = os.listdir(sql_dir)
        for sql_file in sql_files:
            # 定義要匯出的資料表清單
            table_names.append(sql_file.split(".")[0])
            with open(f"{sql_dir}/{sql_file}", "r") as f:
                sql = f.read()
                table_select_sqls.append(sql)

        # 確保 csv 目錄存在
        dirs = "./output/point"
        os.makedirs(dirs, exist_ok=True)

        for table_name in table_names:
            try:
                logger.info(f"正在處理資料表: {table_name}")
                # 透過 table_name 查出對應的查詢 SQL

                table_index = table_names.index(table_name)
                select_sql = table_select_sqls[table_index]

                # 替換代碼 (Token) ##USER_ID## ，因為資料量巨大，改成一次抓一個人的資料，所以這邊不替換
                #select_sql = select_sql.replace("##USER_ID##", source_user_id)

                # 算出今年的年份                
                current_year = get_now().year
                select_sql = select_sql.replace("##YEAR##", str(current_year))

                # 計算出今天的年月日，格式為 YYYY-MM-DD
                today_str = get_now().strftime("%Y-%m-%d")
                select_sql = select_sql.replace("##TODAY##", today_str)

                # 計算出今天第幾周
                now = get_now()
                current_week_sun = get_custom_week_number(now.date(), start_weekday=6)
                current_week_mon = get_custom_week_number(now.date(), start_weekday=0)
                select_sql = select_sql.replace("##WEEK_MON##", str(current_week_mon))
                select_sql = select_sql.replace("##WEEK_SUN##", str(current_week_sun))

                # 計算出今天第幾天
                current_day_mon = now.weekday()
                # 根據規格：星期日=1, 星期一=2, ... 星期六=7
                # weekday(): Mon=0, ... Sun=6
                current_day_sun = (current_day_mon + 1) % 7 + 1
                select_sql = select_sql.replace("##DAY_MON##", str(current_day_mon))
                select_sql = select_sql.replace("##DAY_SUN##", str(current_day_sun))

                logger.debug(f"  計算出 ##YEAR## => {current_year} , ##TODAY## => {today_str} , ##WEEK_MON## => {current_week_mon}, ##WEEK_SUN## => {current_week_sun}, ##DAY_MON## => {current_day_mon} , ##DAY_SUN## => {current_day_sun}")

                # source_user_id 為 `3,13` 的格式
                # source_user_id ，因為資料量巨大，改成一次抓一個人的資料
                # 將 source_user_id 轉成陣列格式
                # 如果 source_user_id 為 `3` ，轉為陣列會有問題嗎?
                # 答案是不會，因為 split 會將 `3` 轉成 `['3']`
                user_ids = source_user_id.split(",")
                for user_id in user_ids:
                    original_sql = select_sql
                    original_sql = original_sql.replace("##USER_ID##", user_id)
                    logger.info(f"正在執行查詢: {original_sql}")

                    columns, data = fetch_data(source_config, original_sql)
                    if data:
                        # 產生一個時間戳記
                        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                        save_to_csv(columns, data, f"{dirs}/{table_name}_{timestamp}.csv")
                        # 同步寫入目標資料庫
                        insert_data(f"{table_name}", columns, data)
                        # 延遲 5 秒再執行下一個，避免資料庫忙碌
                        time.sleep(5)
                    else:
                        logger.warning(f"來源資料庫: {source_config['host']}，資料表 {table_name} user_id:{user_id} 無資料")

            except Exception as e:
                logger.error(f"處理資料表 {table_name} 時發生錯誤: {e}")
    else:
        logger.error("無法連線至資料庫，程式終止。")

