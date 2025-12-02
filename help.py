from datetime import datetime, timedelta, date as datetime_date
import logging


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