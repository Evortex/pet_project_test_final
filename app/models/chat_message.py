from sqlalchemy import Column, Integer, String, ForeignKey, false
from sqlalchemy.orm import relationship

from database import Base


# Модель(сущность базы данных) Chat_message, которая наследуется от класса Base.
class Chat_message(Base):
    # Указываем соответствующее имя таблицы в БД.
    __tablename__ = 'chat_messages'

    # Декларируем столбцы в таблице.
    id = Column(Integer, primary_key=True, index=True)  # Число, первичный ключ, индекс.
    project_id = Column(Integer, ForeignKey("projects.id"))  # Число, внешний ключ из таблицы "projects".
    project = relationship("Project", back_populates="messages")  # Связь "многие к одному" с таблицей "projects".
    message = Column(String)
