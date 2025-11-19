@echo off
echo === Lancement des tests de performance ===

rem Activation du pipenv et lancement du script Python
pipenv run python tests/performance/run_performance_tests.py

pause
