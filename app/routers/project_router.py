from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
import starlette.status as status
from fastapi.responses import RedirectResponse

from schemas.project_dto import Project
from template import templates
from database import get_db
from services import project_service

# Создаем экземпляр класса APIRouter.
router = APIRouter()


# POST обработчик пути /project/ с тегом project, возвращает в ответе HTML страницу.
# Теги нужны для группировки путей в документации, response_class для отображения в документации возвращаемого типа.
@router.post('/', tags=["project"], response_class=HTMLResponse)
# Функция create_project, принимает в параметрах запроса поля проекта,
# а также зависимость от класса Session(сессии с БД).
def create_project(request: Request,
                   name: str = Form(...),
                   category: str = Form(...),
                   description: str = Form(""),
                   author: str = Form(...),
                   db: Session = Depends(get_db)):
    # Создаем экземпляр класса Project и присваиваем его полям значения из параметров запроса.
    project = Project(name=name, category=category, description=description, author=author)

    # Вызываем функцию create_project из project_service, передаем ей экземпляр класса Project и экземпляр сессии.
    project_service.create_project(project, db)

    # Возвращаем редирект на путь /project, с кодом 301 (перемещение на страницу всех проектов).
    return RedirectResponse(request.url_for('get_all_projects'), status_code=status.HTTP_301_MOVED_PERMANENTLY)


# GET обработчик пути /project с тегом project, возвращает в ответе HTML страницу.
@router.get('/', tags=["project"], response_class=HTMLResponse)
# Функция get_all_projects, принимает в параметрах запроса зависимость от класса Session.
def get_all_projects(request: Request, db: Session = Depends(get_db)):
    # Вызываем функцию get_all_projects из project_service, передаем ей экземпляр сессии.
    projects = project_service.get_all_projects(db)

    # Возвращаем рендер шаблона projects.html из папки templates, передаем в него запрос и список всех проектов из БД.
    return templates.TemplateResponse("projects.html", {"request": request, "projects": projects})


# GET обработчик пути /project/{id} с тегом project, возвращает в ответе HTML страницу.
@router.get('/{id}', tags=["project"], response_class=HTMLResponse)
# Функция get_project_by_id, принимает в параметрах запроса id проекта, а также зависимость от класса Session.
def get_project_by_id(request: Request, id: int = None, db: Session = Depends(get_db)):
    # Вызываем функцию get_project_by_id из project_service, передаем ей id проекта и экземпляр сессии.
    project = project_service.get_project_by_id(id, db)

    # Возвращаем рендер шаблона project_page.html из папки templates, передаем в него запрос, id проекта и проект.
    return templates.TemplateResponse("project_page.html", {"request": request, "id": id, "project": project})


# GET обработчик пути /project/{id}update/ с тегом project, возвращает в ответе HTML страницу.
@router.get('/{id}/update', tags=["project"], response_class=HTMLResponse)
# Функция get_project_by_id_for_update, принимает в параметрах запроса id проекта,
# а также зависимость от класса Session.
def get_project_by_id_for_update(request: Request, id: int = None, db: Session = Depends(get_db)):
    # Вызываем функцию get_project_by_id из project_service, передаем ей id проекта и и экземпляр сессии.
    project = project_service.get_project_by_id(id, db)

    # Возвращаем рендер шаблона project_edit_page.html из папки templates, передаем в него запрос, id проекта и проект.
    return templates.TemplateResponse("project_edit_page.html", {"request": request, "id": id, "project": project})


# POST обработчик пути /project/{id}/update с тегом project, возвращает в ответе HTML страницу.
@router.post('/{id}/update', tags=["project"], response_class=HTMLResponse)
# Функция update_project, принимает в параметрах запроса id и остальные поля проекта,
# а также зависимость от класса Session.
def update_project(request: Request,
                   id: int = None,
                   name: str = Form(...),
                   category: str = Form(...),
                   description: str = Form(...),
                   author: str = Form(...),
                   db: Session = Depends(get_db)):
    # Создаем экземпляр класса Project и присваиваем его полям значения из параметров запроса.
    project = Project(name=name, category=category, description=description, author=author, date="")

    # Вызываем функцию update_project из project_service, передаем ей id проекта,
    # экземпляр класса Project и экземпляр сессии.
    project_service.update_project(id, project, db)

    # Возвращаем редирект на путь /project/{id}, с кодом 301.
    return RedirectResponse(request.url_for('get_project_by_id', id=id), status_code=status.HTTP_301_MOVED_PERMANENTLY)


# POST обработчик пути /project/delete/{id} с тегом project, возвращает в ответе HTML страницу.
@router.post('/{id}/delete', tags=["project"], response_class=HTMLResponse)
# Функция delete_project, принимает в параметрах запроса id проекта и зависимость от класса Session.
def delete_project(request: Request, id: int = None, db: Session = Depends(get_db)):
    # Вызываем функцию delete_project из project_service, передаем ей id проекта и экземпляр сессии.
    project_service.delete_project(db, id)

    # Возвращаем редирект на путь /project, с кодом 301
    return RedirectResponse(request.url_for('get_all_projects'), status_code=status.HTTP_301_MOVED_PERMANENTLY)


# POST обработчик пути /project/gpt/{id} с тегом project, возвращает в ответе HTML страницу.
@router.post('/{id}/gpt', tags=["project"], response_class=HTMLResponse)
# Функция ask_gpt, принимает в параметрах запроса id проекта и запрос для GPT, а также зависимость от класса Session.
def ask_gpt(request: Request, id: int = None, gpt_request: str = Form(...), db: Session = Depends(get_db)):
    # Вызываем функцию ask_gpt из project_service, передаем ей id проекта, запрос для GPT и экземпляр сессии.
    project_service.ask_gpt(id, gpt_request, db)

    # Возвращаем редирект на путь /project/{id}, с кодом 301.
    return RedirectResponse(request.url_for('get_project_by_id', id=id), status_code=status.HTTP_301_MOVED_PERMANENTLY)
