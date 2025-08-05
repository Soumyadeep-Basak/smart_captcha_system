@echo off
echo Starting ML-based Flask server WITHOUT MongoDB...
cd /d "d:\hack\botv1\bots"
echo This version uses JSON file storage instead of MongoDB
echo Predictions will be saved to predictions.json
D:\hack\botv1\.venv\Scripts\python.exe script2_no_mongo.py
pause
