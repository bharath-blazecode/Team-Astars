@echo off
setlocal
cd /d "%~dp0"
if not exist "%~dp0run_dashboard.py" goto incomplete_download
if not exist "%~dp0backend\main.py" goto incomplete_download

py -3 -c "import sys; sys.exit(0 if sys.version_info >= (3, 12) else 1)" >nul 2>&1
if not errorlevel 1 goto launch_py

python -c "import sys; sys.exit(0 if sys.version_info >= (3, 12) else 1)" >nul 2>&1
if not errorlevel 1 goto launch_python

echo Python 3.12 or newer was not found.
echo Install Python from https://www.python.org/downloads/windows/
echo Then extract the full project ZIP and double-click START_WINDOWS.cmd again.
pause
exit /b 1

:launch_py
py -3 "%~dp0run_dashboard.py" --demo
goto finished

:launch_python
python "%~dp0run_dashboard.py" --demo

:finished
set "SPEEDQ_EXIT=%ERRORLEVEL%"
if not "%SPEEDQ_EXIT%"=="0" pause
exit /b %SPEEDQ_EXIT%

:incomplete_download
echo Extract the ENTIRE project ZIP with Extract All, then open the extracted folder.
echo START_WINDOWS.cmd must be beside run_dashboard.py and the backend folder.
pause
exit /b 1
