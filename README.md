# Platform-course

Учебный backend-проект образовательной платформы, разработанный на языке **Python** в рамках университетского курса.

Проект демонстрирует базовую логику работы системы онлайн-обучения, включая управление курсами, пользователями и образовательным контентом.

## О проекте

Platform-course — это учебный проект, целью которого было моделирование базовой архитектуры образовательной платформы.

В рамках проекта реализованы основные элементы системы онлайн-обучения: управление курсами, работа с пользователями и организация структуры учебного контента.

Проект был создан для практики разработки backend-логики и проектирования структуры приложения.

---

## Системные требования

Перед началом убедитесь, что у вас установлены следующие компоненты:

- Python 3.9 или выше
- PostgreSQL 13 или выше
- pip (Python package manager)
- Git

---

## Установка и запуск проекта

### 1. Клонировать репозиторий

Склонируйте проект на свою локальную машину:

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```
Шаг 2. Создать и активировать виртуальное окружение
Создание виртуального окружения:

``` bash
python -m venv venv
```

Активация:
``` bash
venv\Scripts\activate
```

Шаг 3. Установить зависимости
```bash
pip install -r requirements.txt
```

Настройка базы данных PostgreSQL
Шаг 4. Создать базу данных и пользователя
Откройте терминал PostgreSQL (например, psql) и выполните команды:

```sql
CREATE DATABASE your_db;
CREATE USER your_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE your_db TO your_user;
```
Замените your_db, your_user, your_password на свои реальные значения.

Шаг 5. Импортировать дамп базы данных
В терминале, находясь в папке проекта, выполните:

```bash
psql -U your_user -d your_db -f dump.sql
```
Если используется Windows и psql не работает, перейдите в папку bin PostgreSQL:

```bash
cd "C:\Program Files\PostgreSQL\15\bin"
.\psql.exe -U your_user -d your_db -f C:\путь\к\проекту\dump.sql
```

Настройка Django
Шаг 6. Настроить подключение к базе данных
Откройте файл platformcourse/settings.py и найдите блок DATABASES. Укажите ваши данные подключения:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

Содержимое репозитория

your_project/ — директория с конфигурацией Django
your_app/ — директория с приложением Django
requirements.txt — список зависимостей Python
dump.sql — дамп базы данных PostgreSQL
README.md — инструкция по установке и запуску
.gitignore — исключает лишние файлы из репозитория
