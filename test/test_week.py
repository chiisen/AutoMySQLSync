from datetime import date, timedelta

def get_week_sun(date_obj):
    """
    邏輯驗證用：計算以星期日為一週開始的週數
    """
    # 找到該年的第一個星期日
    first_day_of_year = date(date_obj.year, 1, 1)
    # 計算第一個星期日是哪一天
    days_to_first_sunday = (6 - first_day_of_year.weekday()) % 7  # weekday: 0=Mon, 6=Sun
    first_sunday = first_day_of_year + timedelta(days=days_to_first_sunday)
    
    # 計算從第一個星期日到當前日期的天數
    days_since_first_sunday = (date_obj - first_sunday).days
    
    # 週數 = 天數 // 7 + 1
    if days_since_first_sunday >= 0:
        week_num = (days_since_first_sunday // 7) + 1
    else:
        week_num = 0 # Placeholder for days before the first Sunday
    
    return week_num

def get_week_mon(date_obj):
    """
    邏輯驗證用：計算以星期一為一週開始的週數
    """
    # 找到該年的第一個星期一
    first_day_of_year = date(date_obj.year, 1, 1)
    # 計算第一個星期一是哪一天
    days_to_first_monday = (0 - first_day_of_year.weekday()) % 7  # weekday: 0=Mon, 6=Sun
    first_monday = first_day_of_year + timedelta(days=days_to_first_monday)
    
    # 計算從第一個星期一到當前日期的天數
    days_since_first_monday = (date_obj - first_monday).days
    
    # 週數 = 天數 // 7 + 1
    if days_since_first_monday >= 0:
        week_num = (days_since_first_monday // 7) + 1
    else:
        week_num = 0 # Placeholder for days before the first Monday
    
    return week_num

# Test cases from docs/var.md
# WEEK_SUN
# 20251115 (Sat) -> 45
# 20251116 (Sun) -> 46
print("--- WEEK_SUN (Logic Verification) ---")
print(f"2025-11-15: {get_week_sun(date(2025, 11, 15))} (Expected: 45)")
print(f"2025-11-16: {get_week_sun(date(2025, 11, 16))} (Expected: 46)")

# WEEK_MON
# 20251116 (Sun) -> 45
# 20251117 (Mon) -> 46
print("\n--- WEEK_MON (Logic Verification) ---")
print(f"2025-11-16: {get_week_mon(date(2025, 11, 16))} (Expected: 45)")
print(f"2025-11-17: {get_week_mon(date(2025, 11, 17))} (Expected: 46)")

# Check ISO week for reference
print("\n--- ISO WEEK (Reference) ---")
print(f"2025-11-16: {date(2025, 11, 16).isocalendar()[1]}")
print(f"2025-11-17: {date(2025, 11, 17).isocalendar()[1]}")
