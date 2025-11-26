

# 編輯 Crontab
在終端機輸入以下指令進入編輯模式：
```bash
crontab -e
```
# 加入排程指令
在文件最下方加入一行。這裡有兩種推薦寫法，建議使用 寫法 A，因為您的程式依賴相對路徑讀取檔案。

## 寫法 A：先切換目錄 (推薦)
這是最穩定的做法，確保 .env、./sql 資料夾都能被正確找到。
- cron
```bash
# 範例：每天早上 8:00 執行，並將輸出存到 log 檔
0 8 * * * cd /root/automysqlsync && /root/automysqlsync/.venv/bin/python auto_day.py >> /root/automysqlsync/cron.log 2>&1
```
```bash
# 範例：每天凌晨 1 點執行
0 1 * * * cd /root/automysqlsync && /usr/bin/python3 auto_day.py >> /root/automysqlsync/cron.log 2>&1
```
- 指令解析：

1. 0 8 * * *: 時間設定 (分 時 日 月 週)。
2. cd /root/automysqlsync: 關鍵步驟，先切換到專案目錄。
3. &&: 確保切換目錄成功後才執行後面的指令。
4. /root/automysqlsync/.venv/bin/python: 使用絕對路徑指定 Python 直譯器 (請依實際情況調整)。
5. auto_day.py : 執行腳本。
6. >> .../cron.log 2>&1: 將標準輸出 (stdout) 和錯誤輸出 (stderr) 都寫入 log 檔，方便除錯。

## 寫法 B：使用 Wrapper Shell Script (進階)
如果您需要設定很多環境變數，或者邏輯較複雜，可以寫一個 shell script 來包裝。

建立 run_day_sync.sh:
```bash
which python3
```
可以查詢 python3 的路徑
```bash
#!/bin/bash
cd /root/automysqlsync
source .venv/bin/activate  # 如果需要激活虛擬環境
python auto_day.py
```
然後在 crontab 中執行這個 .sh 檔：
```bash
0 8 * * * /root/automysqlsync/run_day_sync.sh >> /root/automysqlsync/cron.log 2>&1
```
## 常見問題檢查
1. 權限: 確保 auto_day.py (或 .sh 檔) 有執行權限，雖然直接用 python auto_day.py 不需要 x 權限，但確保目錄可讀寫是必要的。
- chmod +x /root/automysqlsync/auto_day.py
2. 環境變數: 您的程式碼有使用 load_dotenv()，這很好。只要確保 cd 到正確目錄，它就能讀取到 .env。
3.Log 檢查: 設定完成後，建議先將時間設為幾分鐘後，觀察 cron.log 是否有內容產生，以確認是否執行成功。


