@echo off

for /l %%a in (1,1,100) do (
set /p var=����������:
git add *
echo %var%_2
echo git commit -m %var%_2
echo git push origin master
pause
)
