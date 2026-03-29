@echo off
echo ============================================================
echo      S-AOS AUTOMATIC SETUP - KICH HOAT HE THONG
echo ============================================================

:: 1. Kiem tra Python 3.12
py -3.12 --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Khong tim thay Python 3.12! Dang tai va cai dat...
    winget install -e --id Python.Python.3.12
    echo [INFO] Hay khoi dong lai file .bat nay sau khi cai xong Python.
    pause
    exit
)

:: 2. Tao moi truong ao venv
if not exist venv (
    echo [INFO] Dang tao moi truong ao venv (Python 3.12)...
    py -3.12 -m venv venv
) else (
    echo [INFO] venv da ton tai. Bo qua buoc tao.
)

:: 3. Cai dat thu vien
echo [INFO] Dang cai dat cac thu vien can thiet...
call .\venv\Scripts\activate
python -m pip install --upgrade pip
pip install langchain-google-genai google-genai langgraph python-dotenv pydantic openpyxl pandas

:: 4. Kiem tra file .env
if not exist .env (
    echo [WARNING] File .env chua ton tai!
    set /p api_key="Nhap Gemini API Key cua ban: "
    echo GEMINI_API_KEY=%api_key% > .env
    echo [SUCCESS] Da tao file .env voi Key cua ban.
)

echo ============================================================
echo      THIET LAP HOAN TAT! GO 'python main_v1.py' DE CHAY.
echo ============================================================
pause