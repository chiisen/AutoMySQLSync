import os
import sys
import csv
import pymysql
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
    convert_user_id,
    compare_data,
    delete_day_data,
)

script_name = "auto_day_fix"


if __name__ == "__main__":
    if check_db_connection(script_name):
        table_names = []
        table_select_sqls = []

        # 讀出 ./sql/day 目錄下的 SQL 指令  
        sql_dir = "./sql/day"
        sql_files = os.listdir(sql_dir)
        for sql_file in sql_files:
            # 定義要匯出的資料表清單
            table_names.append(sql_file.split(".")[0])
            with open(f"{sql_dir}/{sql_file}", "r") as f:
                sql = f.read()
                table_select_sqls.append(sql)

        # 確保 csv 目錄存在
        dirs = "./output/day_fix"
        os.makedirs(dirs, exist_ok=True)

        # 檢查是否有差異
        is_diff = []
        for table_name in table_names:
            try:
                logger.info(f"正在處理資料表: {table_name}")
                # 透過 table_name 查出對應的查詢 SQL

                table_index = table_names.index(table_name)
                select_sql = table_select_sqls[table_index]

                # 替換代碼 (Token) ##USER_ID##
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

                source_host = source_config['host']
                host = source_host
                source_select_sql = select_sql
                source_select_sql = source_select_sql.replace("##USER_ID##", source_user_id)
                logger.info(f"來源資料庫: {source_host}，正在執行查詢: {source_select_sql}")
                
                source_columns, source_data = fetch_data(source_config, source_select_sql)
                if source_data:
                    save_to_csv(source_columns, source_data, f"{dirs}/{table_name}_source.csv")
                    save_to_csv_with_user_id_mapping(source_columns, source_data, f"{dirs}/{table_name}_source_with_user_id_mapping.csv")
                else:
                    logger.warning(f"來源資料庫: {source_host}，資料表 {table_name} 無資料")


                target_host = target_config['host']
                host = target_host
                target_select_sql = select_sql
                target_select_sql = target_select_sql.replace("##USER_ID##", target_user_id)

                logger.info(f"目標資料庫: {target_host}，正在執行查詢: {target_select_sql}")

                target_columns, target_data = fetch_data(target_config, target_select_sql)
                if target_data:
                    save_to_csv(target_columns, target_data, f"{dirs}/{table_name}_target.csv")
                    save_to_csv_with_user_id_mapping(target_columns, target_data, f"{dirs}/{table_name}_target_with_user_id_mapping.csv")
                else:
                    logger.warning(f"目標資料庫: {target_host}，資料表 {table_name} 無資料")

                # 比對來源和目標資料
                if source_data and target_data:
                    # source_data 需要轉換 user_id，target_data 不需要
                    source_data_with_user_id_mapping = convert_user_id(source_columns, source_data)
                    # 比對來源和目標資料
                    diff_data = compare_data(source_data_with_user_id_mapping, target_data)
                    if diff_data:
                        logger.warning(f"資料表 {table_name} 有差異，正在寫入差異資料到 CSV 檔案")
                        save_to_csv(target_columns, diff_data, f"{dirs}/{table_name}_diff.csv")

                        # 有差異
                        is_diff.append(table_name)

                        # 刪除目標的原始資料
                        delete_day_data(f"{table_name}", current_year, today_str, current_week_mon, current_week_sun, current_day_mon, current_day_sun)

                        # 同步寫入目標資料庫
                        insert_data(f"{table_name}", target_columns, source_data_with_user_id_mapping)
                    else:
                        logger.info(f"資料表 {table_name} 無差異")  
                
            except Exception as e:
                logger.error(f"處理資料庫: {host}，資料表 {table_name} 時發生錯誤: {e}")

        # 執行目錄 ./sql_execute 下的 SQL 指令
        sql_dir = "./sql_execute/day"
        sql_files = os.listdir(sql_dir)
        for sql_file in sql_files:
            try:
                logger.info(f"來源資料庫: {target_config['host']}，正在執行 SQL 指令: {sql_file}")
                with open(f"{sql_dir}/{sql_file}", "r") as f:
                    sql = f.read()

                    # 替換代碼 (Token) ##USER_ID##
                    sql = sql.replace("##USER_ID##", target_user_id)

                    # 算出今年的年份                
                    current_year = get_now().year
                    sql = sql.replace("##YEAR##", str(current_year))

                    # 計算出今天的年月日，格式為 YYYY-MM-DD
                    today_str = get_now().strftime("%Y-%m-%d")
                    sql = sql.replace("##TODAY##", today_str)

                    # 計算出今天第幾周
                    now = get_now()
                    current_week_sun = get_custom_week_number(now.date(), start_weekday=6)
                    current_week_mon = get_custom_week_number(now.date(), start_weekday=0)
                    
                    sql = sql.replace("##WEEK_MON##", str(current_week_mon))
                    sql = sql.replace("##WEEK_SUN##", str(current_week_sun))

                    # 計算出今天第幾天
                    current_day_mon = now.weekday()
                    # 根據規格：星期日=1, 星期一=2, ... 星期六=7
                    # weekday(): Mon=0, ... Sun=6
                    current_day_sun = (current_day_mon + 1) % 7 + 1
                    sql = sql.replace("##DAY_MON##", str(current_day_mon))
                    sql = sql.replace("##DAY_SUN##", str(current_day_sun))

                    logger.debug(f"  計算出 ##YEAR## => {current_year} , ##TODAY## => {today_str} , ##WEEK_MON## => {current_week_mon}, ##WEEK_SUN## => {current_week_sun}, ##DAY_MON## => {current_day_mon}, ##DAY_SUN## => {current_day_sun} ")

                    logger.info(f"來源資料庫: {target_config['host']}，正在執行統計 SQL 指令: {sql_file}")

                    # 執行 SQL 指令
                    if is_diff:
                        # 判斷 is_diff 之中是否包含 sql_file
                        for sql_file in is_diff:
                            logger.info(f"來源資料庫: {target_config['host']}，正在執行統計 SQL 指令: {sql_file}")
                            execute_sql(sql)
            except Exception as e:
                logger.error(f"執行 SQL 指令 {sql_file} 時發生錯誤: {e}")
    else:
        logger.error("無法連線至資料庫，程式終止。")

