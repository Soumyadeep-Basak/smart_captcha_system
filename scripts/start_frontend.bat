@echo off
echo Starting Frontend Development Server...
cd /d "d:\hack\botv1\frontend"

if not exist "node_modules" (
    echo Installing frontend dependencies...
    npm install
)

echo Starting Next.js development server...
npm run dev
pause
