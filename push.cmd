@echo off

for /l %%a in (1,1,100) do (
set /p var=ÇëÊäÈëÄÚÈİ:
git add *
git commit -m %var%_1
git push origin master
pause
)
