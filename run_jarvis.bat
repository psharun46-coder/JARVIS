@echo off
color 0b
title Jarvis Web Interface
echo ===================================================
echo               JARVIS IS BOOTING THE HUD...
echo           Please Wait for the Browser to open
echo ===================================================
cd /d "c:\Users\ACER\OneDrive\Desktop\jarvis"
start http://localhost:5000
python app.py
pause
