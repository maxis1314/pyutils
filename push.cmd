@echo off
set /p var=����������:
git add *
git commit -m %var%_1
git push origin master
pause