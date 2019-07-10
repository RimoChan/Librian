@echo off
set koko=%CD%
cd ../..
.\python36\python.exe -m Librian.py --project %koko%
pause
