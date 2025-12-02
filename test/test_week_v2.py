from datetime import date
import sys
import os

# Add parent directory to sys.path to import auto_day
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from help import (
    get_custom_week_number
)

# Test cases from docs/var.md
# WEEK_SUN (start_weekday=6)
# 20251115 (Sat) -> 45
# 20251116 (Sun) -> 46
print("--- WEEK_SUN (Implementation Verification: start_weekday=6) ---")
print(f"2025-11-15: {get_custom_week_number(date(2025, 11, 15), start_weekday=6)} (Expected: 45)")
print(f"2025-11-16: {get_custom_week_number(date(2025, 11, 16), start_weekday=6)} (Expected: 46)")

# WEEK_MON (start_weekday=0)
# 20251116 (Sun) -> 45
# 20251117 (Mon) -> 46
print("\n--- WEEK_MON (Implementation Verification: start_weekday=0) ---")
print(f"2025-11-16: {get_custom_week_number(date(2025, 11, 16), start_weekday=0)} (Expected: 45)")
print(f"2025-11-17: {get_custom_week_number(date(2025, 11, 17), start_weekday=0)} (Expected: 46)")
