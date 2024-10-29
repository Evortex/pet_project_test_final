import uvicorn
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from fastapi import Request
from fastapi.responses import HTMLResponse

from routers.project_router import router as project_router
from template import templates


# Функция создания экземпляра приложения FastAPI.
def create_app():
    # Создаем экземпляр приложения FastAPI.
    app = FastAPI()
    # Подключаем роутер проектов.
    app.include_router(project_router, prefix='/project')
    # Подключаем директорию со статическими файлами.
    app.mount("/static", StaticFiles(directory="static"), name="static")

    # Возвращаем экземпляр приложения.
    return app


# Присваиваем глобальной переменной app экземпляр приложения.
app = create_app()


# GET обработчик корневого пути / с тегом root, возвращает в ответе HTML страницу.
@app.get('/', tags=["root"], response_class=HTMLResponse)
# Функция обработчик корневого пути.
def get_index(request: Request):
    # Возвращаем рендер шаблона index.html из папки templates, передаем в него запрос.
    return templates.TemplateResponse("index.html", {"request": request})


# Оператор запуска приложения.
if __name__ == '__main__':
    # Запуск сервера uvicorn из приложения app, по адресу 0.0.0.0:8080,
    # с автоматической перезагрузкой при изменении кода и 3 воркерами.
    uvicorn.run("main:app", host='0.0.0.0', port=8080, reload=True, workers=3)
