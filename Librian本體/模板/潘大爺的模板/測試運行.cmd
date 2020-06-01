@echo off
set koko=%CD%
cd ../..
..\python36\python.exe Librian.py --project %koko%
pause
