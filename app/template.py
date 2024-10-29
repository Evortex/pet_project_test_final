from fastapi.templating import Jinja2Templates

# Создаем экземпляр класса Jinja2Templates и передаем ему путь к папке с шаблонами,
# присваиваем глобальной переменной templates.
templates = Jinja2Templates(directory="templates")
