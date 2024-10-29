import os

from sqlalchemy.orm import Session
import openai

from models.chat_message import Chat_message
from schemas import project_dto
from models.project import Project

# Устанавливаем API-ключ OpenAI, получаем его из переменной окружения API_KEY.
openai.api_key = os.getenv("API_KEY")
# Устанавливаем модель OpenAI, в данном случае используем gpt-3.5-turbo.
model_engine = "gpt-3.5-turbo"


# Функция для создания проекта, принимает в качестве аргументов DTO класса Project и экземпляр класса Session.
def create_project(project_dto: project_dto.Project, db: Session):
    # Создаем экземпляр класса Project, используя данные из project_dto.
    project = Project(name=project_dto.name, category=project_dto.category,
                      description=project_dto.description, author=project_dto.author)

    # Пытаемся выполнить код в блоке try.
    try:
        # Добавляем экземпляр класса Project в сессию.
        db.add(project)
        # Коммитим изменения в БД.
        db.commit()
        # Обновляем экземпляр класса Project.
        db.refresh(project)
    except Exception as e:
        # Если произошла ошибка, выводим ее в консоль.
        print(e)

    # Возвращаем сохраненный экземпляр класса Project.
    return project


# Функция для получения всех проектов, принимает в качестве аргумента экземпляр класса Session.
def get_all_projects(db: Session):
    # Получаем все проекты из БД, используя метод query().all(), затем возвращаем их.
    return db.query(Project).all()


# Функция для получения проекта по id, принимает в качестве аргументов id проекта и экземпляр класса Session.
def get_project_by_id(id: int, db: Session):
    # Получаем проект из БД, используя метод query().get(), затем возвращаем его.
    return db.query(Project).get(id)


# Функция для обновления проекта, принимает в качестве аргументов id проекта,
# DTO класса Project и экземпляр класса Session.
def update_project(id: int, project_dto: project_dto.Project, db: Session):
    # Получаем проект из БД, используя метод query().get().
    project = db.query(Project).get(id)

    # Обновляем поля проекта, используя данные из project_dto.
    project.name = project_dto.name
    project.category = project_dto.category
    project.description = project_dto.description
    project.author = project_dto.author

    # Пытаемся выполнить код в блоке try.
    try:
        # Добавляем экземпляр класса Project в сессию.
        db.add(project)
        # Коммитим изменения в БД.
        db.commit()
        # Обновляем экземпляр класса Project.
        db.refresh(project)
    except Exception as e:
        # Если произошла ошибка, выводим ее в консоль.
        print(e)

    # Возвращаем обновленный экземпляр класса Project.
    return project


# Функция для удаления проекта, принимает в качестве аргументов id проекта и экземпляр класса Session.
def delete_project(db: Session, id: int):
    # Получаем проект из БД, используя метод query().get().
    project = db.query(Project).get(id)

    try:
        # Удаляем все сообщения из истории чата проекта.
        for message in project.messages:
            db.delete(message)
        # Удаляем проект.
        db.delete(project)
        # Коммитим изменения в БД.
        db.commit()
    except Exception as e:
        # Если произошла ошибка, выводим ее в консоль.
        print(e)

    # Возвращаем удаленный экземпляр класса Project.
    return project


# Функция для отправки запросов к ChatGPT API и сохранения истории переписки в таблицу chat_messages,
# принимает в качестве аргументов id проекта, запрос к GPT и экземпляр класса Session.
def ask_gpt(id: int, gpt_request: str, db: Session):
    # Получаем проект из БД, используя метод query().get().
    project = db.query(Project).get(id)

    # Получаем последние 6 сообщений переписки, используя фильтрацию по id проекта,
    # обратную сортировку и лимитирование.
    # Сортируем полученные сообщения по id.
    last_six_messages = sorted((db.query(Chat_message)
                                .filter_by(project_id=project.id)
                                .order_by(Chat_message.id.desc())
                                .limit(6).all()), key=lambda x: x.id)

    # Собираем историю переписки в массив строк для передачи ее в запрос к ChatGPT API(поддержка контекста).
    chat_history = [chat_message.message for chat_message in last_six_messages]

    # Отправляем запрос к ChatGPT по API, используя метод openai.ChatCompletion.create().
    gpt_response = openai.ChatCompletion.create(
        model=model_engine,
        messages=[
            {"role": "user", "content": "User and GPT previous conversation context(DONT INCLUDE IT IN RESPONSE): "
                                        + ''.join(chat_history)
                                        + " | New request(REPLY FOR THIS, USING PREVIOUS CONVERSATION CONTEXT): "
                                        + gpt_request + " |"},
        ]
    ).choices[0].message.content

    # Добавляем запрос в историю переписки проекта.
    request = Chat_message(message="Вы: " + gpt_request, project=project)
    # Добавляем ответ в историю переписки проекта.
    response = Chat_message(message="GPT: " + gpt_response, project=project)

    # Пытаемся выполнить код в блоке try
    try:
        # Добавляем экземпляр request, response и project в сессию.
        db.add(request)
        db.add(response)
        db.add(project)
        # Коммитим изменения в БД.
        db.commit()
        # Обновляем экземпляр класса Project.
        db.refresh(project)
    except Exception as e:
        # Если произошла ошибка, выводим ее в консоль.
        print(e)

    # Возвращаем обновленный экземпляр класса Project.
    return project
