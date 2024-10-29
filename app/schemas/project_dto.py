from pydantic import BaseModel, Field


# DTO(Data Transfer Object) модели Project.
class Project(BaseModel):
    # Указываем поля DTO, которые будут соответствовать полям модели Project, не включая id.
    # Они будут использоваться для валидации данных, передаваемых в запросе.
    # Все поля обязательны для заполнения.
    name: str = Field(max_length=60)  # Строка, максимальной длины 60 символов.
    category: str = Field(max_length=15)  # Строка, максимальной длины 15 символов.
    description: str = Field(max_length=400)  # Строка, максимальной длины 400 символов.
    author: str
