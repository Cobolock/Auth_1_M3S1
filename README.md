# Проектное задание: Сервис авторизации

## Запуск (Development)

Сервисы в docker-compose.yaml имеют следующие профили:
- `etl`
- `movies-api`
- `movies-admin`
- `auth`
  - `auth-infra`

Запустить сервис авторизации можно следующей командой:

```bash
COMPOSE_PROFILES=auth docker-compose -f docker-compose.yml -f docker-compose.override.yml up --build -d
```

Можно выбрать сразу несколько профилей для запуска через запятую.
Например, запустить все сервисы разом можно следующей командой:

```bash
COMPOSE_PROFILES=etl,movies-api,movies-admin,auth docker-compose -f docker-compose.yml -f docker-compose.override.yml up --build -d
```

Для остановки всех сервисов выполните команду:

```bash
COMPOSE_PROFILES=etl,movies-api,movies-admin,auth docker-compose -f docker-compose.yml -f docker-compose.override.yml down
```

Для удаления всех данных БД (volumes) можно добавить флаг `-v`:

```bash
COMPOSE_PROFILES=etl,movies-api,movies-admin,auth docker-compose -f docker-compose.yml -f docker-compose.override.yml down -v
```

## Запуск (Production)

Сервис авторизации

```bash
COMPOSE_PROFILES=auth docker-compose up --build -d
```

Все сервисы

```bash
COMPOSE_PROFILES=etl,movies-api,movies-admin,auth docker-compose up --build -d
```

## Сервисы

| Название сервиса     | Внешний адрес (localhost)                                   | Внутренний адрес (docker network)                               |
|----------------------|-------------------------------------------------------------|-----------------------------------------------------------------|
| Movies API           | http://127.0.0.1:8000/api/docs                              | http://movies-api:8000/api/docs                                 |
| Movies API (Nginx)   | http://127.0.0.1:7000/api/docs                              | http://movies-api-nginx/api/docs                                |
| Movies PostgreSQL    | `postgres://app:123qwe@localhost:5432/movies_database`      | `postgres://app:123qwe@movies-postgres:5432/movies_database`    |
| Movies Redis         | `redis://localhost:6379`                                    | `redis://movies-redis:6379`                                     |
| Movies Admin         | http://127.0.0.1:8001/admin                                 | http://movies-admin:8000/admin                                  |
| Movies Admin (Nginx) | http://127.0.0.1:7001/admin                                 | http://movies-admin-nginx:80/admin                              |
| Auth API             | http://127.0.0.1:8002/api/docs                              | http://auth-api:8000/api/docs                                   |
| Auth API (Nginx)     | http://127.0.0.1:7002/api/docs                              | http://auth-api-nginx:80/api/docs                               |
| Auth PostgreSQL      | `postgres://auth_user:auth_password@localhost:5433/auth_db` | `postgres://auth_user:auth_password@auth-postgres:5432/auth_db` |
| Auth Redis           | `redis://localhost:6380`                                    | `redis://auth-redis:6379`                                       |
| Jaeger UI            | http://127.0.0.1:16686/search                               | http://auth-jaeger:16686/search                                 |
