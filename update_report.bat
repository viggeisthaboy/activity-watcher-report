REM Activate virtual environment
call "C:\Users\vigge\.Coding\Moce-DV\Python\.venv\Scripts\activate.bat"

REM Run Python script
python "C:\Users\vigge\.Coding\Moce-DV\Python\export_activity Github.py"

REM Navigate to project directory
cd "C:\Users\vigge\.Coding\Moce-DV\Python"

REM Add index.html to Git
git add index.html

REM Commit changes
git commit -m "Daily report update"

REM Push to GitHub
git push origin main