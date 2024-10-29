#!/bin/sh
# Переходим в директорию app.
cd app
# Применяем миграции.
pipenv run alembic upgrade head
# Запускаем приложение (миграции применяются автоматически на старте).
pipenv run python main.py
