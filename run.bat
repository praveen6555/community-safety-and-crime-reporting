@echo off
title CrimeGuard AI - Crime Analysis & Predictive Platform
echo =========================================================
echo    Activating Virtual Environment & Starting Server
echo =========================================================
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
) else if exist application\venv\Scripts\activate.bat (
    call application\venv\Scripts\activate.bat
)
python manage.py runserver 127.0.0.1:8000
pause
