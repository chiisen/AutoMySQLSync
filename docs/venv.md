建立 .venv (Python 虛擬環境) 的標準做法是使用 Python 內建的 venv 模組。這能讓您的專案擁有獨立的套件環境，不會與系統或其他專案衝突。

以下是建立與設定的步驟，包含 Windows (您目前的開發環境) 與 Ubuntu/Linux (您的部署環境) 的指令：

# 1. 建立虛擬環境
在專案根目錄 (AutoMySQLSync) 下執行以下指令。這會產生一個名為 .venv 的資料夾。
```bash
# Windows / Linux / macOS 通用
python -m venv .venv
```
(注意：在 Ubuntu 上如果出現錯誤，可能需要先安裝 sudo apt-get install python3-venv)

# 2. 啟動虛擬環境
建立後，必須「啟動」它，終端機前綴會出現 (.venv) 字樣。
- Windows (PowerShell):
```powershell
.\.venv\Scripts\Activate.ps1
```
(若遇到權限錯誤，可先執行 Set-ExecutionPolicy RemoteSigned -Scope Process)
- Windows (CMD):
```cmd
.\.venv\Scripts\activate.bat
```
- Ubuntu / Linux / macOS:
```bash
source .venv/bin/activate
```
# 3. 安裝套件
啟動環境後，根據您的 requirements.txt 安裝所需套件 (如 pymysql, python-dotenv)：
```bash
pip install -r requirements.txt
```
# 4. 離開虛擬環境
```bash
deactivate
```

---

補充：為什麼在 Crontab 裡要寫 .venv/bin/python？
在 Crontab 中，我們通常不執行「啟動 (activate)」的動作，而是直接使用虛擬環境內的 Python 執行檔。

只要指定 /path/to/.venv/bin/python (Linux) 或 .../.venv/Scripts/python.exe (Windows)，程式執行時就會自動使用該虛擬環境內安裝的套件，這就是為什麼在 Crontab 設定中要寫完整路徑的原因。


