@echo off
set PYTHONPATH=%~dp0
pylint --rcfile=linter/pylintrc_recipe %*