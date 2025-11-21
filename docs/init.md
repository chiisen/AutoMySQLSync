# 建立 Python 3.9 的虛擬環境
檢查一下 python 版本
```bash
python --version
```

建立虛擬環境    
```bash
python -m venv .venv
```

啟動虛擬環境
- PowerShell (推薦)
```bash
.\.venv\Scripts\Activate.ps1
``` 
- cmd
```bash
.\.venv\Scripts\Activate
```
提示： 啟動成功後，您的終端機提示字元前方會出現 (.venv) 的標示。 如果在 PowerShell 遇到權限錯誤 (例如 Running scripts is disabled on this system)，您可以嘗試先執行 Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process 來暫時允許執行腳本。

安裝套件
```bash
pip install pymysql
```
```bash
pip install python-dotenv
```
有可能提示 pip 要升級 pip
```bash
python -m pip install --upgrade pip
```

建立 requirements.txt
```bash
pip freeze > requirements.txt
```
套件安裝完全相同的環境
```bash
pip install -r requirements.txt
```

