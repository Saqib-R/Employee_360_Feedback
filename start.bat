@echo off
echo Starting Flask Backend...
cd ./Backend
start cmd /k "flask run"

echo Starting Angular Frontend...
cd ./Frontend
start cmd /k "ng serve"

echo Both applications are starting...
