# Указываем версию Python.
FROM python:3.10
# Указываем рабочую директорию.
WORKDIR /app
# Копируем файлы в рабочую директорию.
COPY . .
# Устанавливаем зависимости.
RUN pip install pipenv && pipenv install --deploy --ignore-pipfile
# Открываем порт.
EXPOSE 8080
# Делаем скрипт исполняемым.
RUN chmod +x entrypoint.sh
# Запускаем скрипт - точку входа в приложение.
ENTRYPOINT ["./entrypoint.sh"]