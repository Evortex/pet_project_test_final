# Урок 7: Деплой приложения на Render

У тебя получился отличный проект, который теперь можно развернуть на сервере Render. Он станет общедоступен, ты сможешь 
поделиться им с друзьями и коллегами, а также использовать в своем портфолио.

## Задание:

1.  Добавь этот проект в свой репозиторий на GitLab.

2. Перейди на render.com и создай новый проект по шаблону Web Service, 
используя свой репозиторий на GitLab в качестве источника.

3. Присвой своему проекту имя

4. В качестве root директории укажи `app`.


5. В качестве build команды укажи приведенный ниже набор.
Дело в том, что мы собираем окружение с нуля, и нам приходится устанавливать множество компонентов.
```
pip install pipenv && pip install uvicorn && pip install importlib-resources && pip install frozenlist && pipenv install --deploy --ignore-pipfile
```

6. В качестве команды запуска укажи `pipenv run alembic upgrade head && pipenv run python main.py`.
Здесь мы сначала применяем миграции к базе данных, а затем запускаем приложение.

Почти готово! Но проект не заработает без базы данных и интеграции с GPT, поэтому добавим их.

7. Перейди в меню проектов и создай PostgreSQL базу данных.

8. Открой страницу базы данных и в блоке Connections скопируй External Database URL, поменяй в нем префикс, 
указывающий на используемый драйвер, на postgresql+psycopg2://.
```
postgres:// -> postgresql+psycopg2://
```

9. Вернись в проект веб-сервиса и во вкладке Environment добавь переменную POSTGRES_DB_URL с ранее скопированным значением.

10. Также добавь переменную API_KEY со значением ключа, который ты использовал в предыдущем уроке.

11. В правом верхнем углу страницы проекта нажми кнопку Manual Deploy-->Deploy latest commit.

12. Теперь давай поймем, как же приложение подбирает переменные из окружения и понимает, к какой базе данных подключиться
и какой ключ использовать. Посмотри строку 9 в файле [database.py](app/database.py), она содержит получение переменной
окружения с помощью команды os.getenv. Также посмотри строку 11 в файле [project_service.py](app/services/project_service.py), 
она содержит то же самое. Таким образом, ты можешь использовать переменные окружения в любом месте своего приложения.
Набор необходимых переменных для запуска приложения и пример их значений, как правило, можно найти
в файле .env.example в корне проекта. Помимо удобства, переменные окружения также необходимо использовать,
чтобы не хранить в коде конфиденциальные данные, такие как ключи доступа к сервисам и базам данных.

13. А еще ты можешь развернуть приложение с базой данных локально, используя docker-compose. Обрати внимание на Dockerfile,
в котором собирается образ приложения и обновленный docker-compose.yml, запускающий контейнеры приложения и бд вместе.
Чтобы запустить приложение локально открой `.env.local`, укажи API_KEY внутри файла и запусти docker-compose.

Супер! Твой проект развернут на общедоступном сервере и доступен всем в интернете. 

### Важные примечания:

1. Для того чтобы корректно начать работу зайди в настройки 
(File-->Settings-->Project-->ProjectStructure) и пометь директорию app в качестве Sources. 
Это нужно, чтобы программа могла правильно видеть файлы внутри проекта.
2. Перед запуском проекта не забудь установить все зависимости из Pipfile.lock.
3. Пиши свой код только внутри отведенных областей между комментариями, 
каждая область помечена номером, соответствующим номеру задания и содержит обозначения границ ("начало" и "конец").
4. Пользуйся поисковыми системами и сервисом Chat GPT, чтобы быстрее находить решения.


###### В директории examples ты можешь найти решения заданий, но мы рекомендуем попытаться решить их самостоятельно.