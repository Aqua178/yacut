### YACUT

Проект YaCut — это сервис укорачивания ссылок. Его назначение — ассоциировать
длинную пользовательскую ссылку с короткой, которую предлагает сам пользователь
или предоставляет сервис.

## Технологии

* python

* flask

* flask-sqlalchemy

* alembic

* flask-WTF

# Запуск проекта

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Aqua178/yacut.git
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

# Запуск приложения и применение миграций

1) Применение миграций: `flask db upgrade`

2) Запуск приложения: `flask run`

# Доступные запросы

1) Создание короткой ссылки (POST-запрос /api/id/):

```json
{
  "url": "string",
  "custom_id": "string"
}
```

Ответ при успешном запросе:

```json
{
  "url": "string",
  "short_link": "string"
}
```

Коды запросов: 201, 400.

2) Получение оригинальной ссылки (GET-запрос /api/{id}/):

Ответ при успешном запросе:
```json
{
  "url": "string"
}
```

Коды запросов: 200, 404.

### Author:
[Vladyka Aleksei](https://github.com/aqua178)