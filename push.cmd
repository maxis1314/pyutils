@echo off

for /l %%a in (1,1,100) do (
set /p var=����������:
git add *
git commit -m %var%_%date%
git push origin master
pause
)
