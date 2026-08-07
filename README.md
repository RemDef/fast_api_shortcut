```
  ______           __       
 /_  __/___ ______/ /_______
  / / / __ `/ ___/ //_/ ___/
 / / / /_/ (__  ) ,< (__  ) 
/_/  \__,_/____/_/|_/____/  
```

# Tasks API

Учебный REST API для задач и пользователей на FastAPI: JWT-авторизация, фильтры и пагинация, агрегации в Postgres, кэш списка в Redis, rate limit, Sentry, Docker.

## Стек

| Слой | Технологии |
|------|------------|
| API | FastAPI, Pydantic v2, Uvicorn / Gunicorn (`UvicornWorker`) |
| БД | PostgreSQL 16, SQLAlchemy 2 (async), Alembic |
| Кэш / лимиты | Redis |
| Auth | JWT (`python-jose`), bcrypt-хеш паролей |
| Наблюдаемость | logging middleware, Sentry |
| Тесты | pytest, pytest-asyncio, httpx, factory-boy |
| Качество | ruff, prek |
| Деплой | Docker, docker-compose |

## Что умеет

- Регистрация пользователей и login с выдачей JWT
- CRUD задач в рамках текущего пользователя
- Список задач: фильтры, поиск, сортировка, `limit`/`offset`, обёртка `count` / `next` / `previous` / `results`
- Кэш списка задач в Redis + инвалидация при create/update/delete
- Статистика: total, by-day, active-users, dashboard (`asyncio.gather`)
- Админские эндпоинты пользователей (`require_admin`)
- Rate limit по IP / user_id из JWT
- Миграции Alembic при старте контейнера

## Быстрый старт (Docker)

```bash
cp .env.example .env   # или свой .env
docker compose up --build
```

- API: http://localhost:7995  
- Swagger: http://localhost:7995/docs  
- Health: http://localhost:7995/check_site  

Внутри compose для `api` уже заданы:

- `DB_URL=postgresql+asyncpg://app:app@db:5432/app`
- `REDIS_URL=redis://redis:6379/0`

На Windows, если локальный Postgres занял `5432`, в compose порт БД проброшен как `5433:5432`. Для команд **с хоста** в `.env` используй `localhost:5433`.

## Переменные окружения

| Переменная | Назначение |
|------------|------------|
| `DB_URL` | async URL БД (`postgresql+asyncpg://...`) |
| `REDIS_URL` | Redis |
| `JWT_SECRET_KEY` | секрет подписи JWT |
| `SENTRY_DSN` | DSN Sentry (опционально) |
| `RATE_LIMIT_REQUESTS` | N запросов |
| `RATE_LIMIT_SECONDS` | за T секунд |

## API (v1)

Базовый префикс: `/v1`

### Auth

| Method | Path | Описание |
|--------|------|----------|
| `POST` | `/v1/auth/login` | логин (form: `username`, `password`) → JWT |

### Users

| Method | Path | Auth | Описание |
|--------|------|------|----------|
| `POST` | `/v1/users/register` | — | регистрация |
| `GET` | `/v1/users/` | admin | список (пагинация) |
| `GET` | `/v1/users/{user_id}` | admin | пользователь по id |
| `DELETE` | `/v1/users/{user_id}` | admin | удалить пользователя |

### Tasks

| Method | Path | Auth | Описание |
|--------|------|------|----------|
| `POST` | `/v1/tasks/` | user | создать задачу |
| `GET` | `/v1/tasks/` | user | список (фильтры + пагинация + cache) |
| `GET` | `/v1/tasks/{task_id}` | user | задача по id (только своя) |
| `PATCH` | `/v1/tasks/{task_id}` | user | обновить |
| `DELETE` | `/v1/tasks/{task_id}` | user | удалить |
| `GET` | `/v1/tasks/stats/total` | user | выполнено / не выполнено / % |
| `GET` | `/v1/tasks/stats/by-day` | user | группировка по дням |
| `GET` | `/v1/tasks/active-users` | admin | топ по открытым задачам |
| `GET` | `/v1/tasks/dashboard` | admin | total + by-day + active-users |

#### Query для `GET /v1/tasks/`

`limit`, `offset`, `is_done`, `created_from`, `created_to`, `order_by` (`created_at` \| `updated_at` \| `title`), `direction` (`asc` \| `desc`), `search`

### Служебные

| Method | Path | Описание |
|--------|------|----------|
| `GET` | `/check_site` | ping |
| `GET` | `/sentry-debug` | тестовая ошибка для Sentry |
| `GET` | `/docs` | Swagger UI |

## Локальная разработка

```bash
uv sync
# поднять db + redis (или весь compose)
uv run alembic upgrade head
uv run uvicorn main:app --reload --port 7995
```

Тесты:

```bash
uv run pytest tests/ -v
```

Миграции:

```bash
uv run alembic revision --autogenerate -m "message"
uv run alembic upgrade head
```

## Структура

```
api/v1/          # эндпоинты (auth, users, tasks)
auth/            # JWT
cache/           # Redis backend, rate limit helpers
common/          # Base model, pagination, errors
middleware/      # logging, rate limit, redact
tasks/           # models, services, cache keys
users/           # models, services, security
alembic/         # миграции
tests/           # pytest + factories + fake cache
```

by Remore
