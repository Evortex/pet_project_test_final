import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Получаем URL для подключения к БД из переменной окружения POSTGRES_DB_URL,
# присваиваем его глобальной переменной(константе) SQLALCHEMY_URL.
SQLALCHEMY_URL = os.getenv("POSTGRES_DB_URL")

# Создаем экземпляр класса Engine для подключения к БД.
engine = create_engine(SQLALCHEMY_URL)
# Собираем экземпляр класса SessionLocal для работы с сессиями, с отключенным автофлашем и автокоммитом.
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)
# Создаем экземпляр класса Base для создания моделей.
Base = declarative_base()


# Функция для получения экземпляра класса SessionLocal.
def get_db():
    # Создаем локальную переменную db, которая будет хранить экземпляр класса SessionLocal.
    db = SessionLocal()

    # Пытаемся выполнить код в блоке try, в любом случае выполняем код в блоке finally.
    try:
        # Возвращаем экземпляр класса SessionLocal.
        yield db
    finally:
        # Всегда после работы закрываем соединение с БД.
        db.close()
