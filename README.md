# Телеграмм бот для сбора участников на боевые мероприятия

Это шаблон для создания телеграмм бота с использованием библиотеки **aiogram**. В проекте используется **MySQL**, **Redis**, и **SQLAlchemy** с поддержкой репликации для хранения данных. Также включены миграции с **Alembic** для управления базой данных.

## Возможности

- **Telegram Bot**: Использование библиотеки `aiogram` для создания и управления телеграмм-ботом.
- **Репликация MySQL**: Использование **MySQL** с репликацией для масштабируемости.
- **Redis**: Использование **Redis** для кэширования и быстрой работы с данными.
- **SQLAlchemy**: ORM для работы с базой данных и поддержка репликации.
- **Миграции Alembic**: Использование Alembic для управления схемой базы данных и миграциями.

## Установка

1. Клонируйте репозиторий:

   ```bash
   git clone https://github.com/hexdevop/fights_registrator_bot.git
   cd fights_registrator_bot
   ```

2. Создайте и активируйте виртуальное окружение:
   - Для Linux:
      ```bash
      python3 -m venv venv
      source venv/bin/activate
      ```
   - Для Windows:
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```

3. Установите зависимости:

   ```bash
   pip install -r requirements.txt
   ```

4. Настройте конфигурацию:
   - Заполните файл `.env` с вашими данными:
     - `bot.token` — токен вашего бота.
     - Данные для подключения к базе данных MySQL и Redis.

5. Запустите миграции Alembic для настройки базы данных:

   ```bash
   alembic upgrade head
   ```

6. Запуск

    ```bash
    python main.py
    ```

## Структура проекта

- **bot/** — Основная логика бота, обработчики, middlewares, и другие утилиты.
- **config.py** — Конфигурация проекта.
- **database/** — Модели SQLAlchemy и настройки подключения к базе данных.
- **migrations/** — Миграции Alembic.

## Миграции базы данных

Для работы с базой данных используется **SQLAlchemy** и **Alembic** для миграций. Чтобы создать новую миграцию, выполните команду:

```bash
alembic revision --autogenerate -m "description of changes"
```

Для применения миграций:

```bash
alembic upgrade head
```

## Используемые технологии

- **aiogram** — библиотека для создания телеграмм-ботов.
- **MySQL** — база данных с поддержкой репликации.
- **SQLAlchemy** — ORM для работы с базой данных.
- **Alembic** — инструмент для миграций базы данных.
- **Redis** — система кэширования.

## Лицензия

Этот проект распространяется под лицензией MIT. См. файл `LICENSE` для подробностей.

