@echo off

rem for /l %%a in (1,1,100) do (
set /p var=ÇëÊäÈëÄÚÈÝ:
git add *
git commit -m "%var% %date:~0,10%"
git push origin master
rem pause
ping 127.0.0.1 -n 10 > nul
rem )
