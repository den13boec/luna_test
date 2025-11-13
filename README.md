# API of organisations directory

REST API-сервис - справочник по организациям, зданиям и видам деятельности. Реализован на FastAPI + SQLAlchemy + Alembic + PostgreSQL, обёрнут в Docker, автосидинг и авторизация по API-ключу.

## ⚙️ Как запустить проект

> Требования: установлен [Docker](https://www.docker.com/) и [Docker Compose](https://docs.docker.com/compose/)

```bash
git clone https://github.com/den13boec/luna_test
cd luna_test
```

Перед запуском необходимо создать .env файл в корне проекта для подключения к БД и авторизации по API-ключу:

```env
# API-ключ для заголовка X-API-Key
API_KEY=supersecretkey

# Postgres
POSTGRES_DB=orgs
POSTGRES_USER=orgs_user
POSTGRES_PASSWORD=orgs_pass
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

Запуск:

```bash
docker compose up --build
```

> Приложение: http://127.0.0.1:8000
>
> Swagger UI: http://127.0.0.1:8000/docs
>
> ReDoc: http://127.0.0.1:8000/redoc

Все ручки (кроме /health) требуют заголовок:

```env
X-API-Key: <значение из .env>
```

В Swagger UI можно ввести API-ключ в форме авторизации, чтобы затем он автоматически припреплялся к обращению на эндпойнты.

## Эндпойнты

|  Метод | URL               | Описание                             |
|:------:|-------------------|--------------------------------------|
| GET    | `/health`         | Проверка доступности (без API-ключа) |

### Здания (buildings)

|  Метод | URL               | Описание                             |
|:------:|-------------------|--------------------------------------|
| GET    | `/buildings`      | Список всех зданий                   |

### Деятельности (activities)

|  Метод | URL                         | Описание                                |
|:------:|-----------------------------|-----------------------------------------|
| GET    | `/activities`               | Плоский список видов деятельности      |
| GET    | `/activities/tree`          | Дерево видов деятельности (≤ 3 уровней). Поддерживается root_id в запросе для выдачи поддерева|
| GET    | `/activities/{activity_id}` | Карточка вида деятельности по ID        |

### Организации (organizations)

|  Метод | URL                                                | Описание                                      |
|:------:|----------------------------------------------------|-----------------------------------------------|
| GET    | `/organizations/by-id/{org_id}`                    | Карточка организации по ID                    |
| GET    | `/organizations/by-building/{building_id}`         | Организации в указанном здании                |
| GET    | `/organizations/search?name=…`                     | Поиск организаций по подстроке в названии     |
| GET    | `/organizations/by-activity-name?name=…&deep=true` | Организации по названию вида деятельности. При deep=true включаются все дочерние виды деятельности |
| GET    | `/organizations/near?lat=…&lon=…&radius_km=…` | Организации в радиусе (км) от точки. Расстояние считается по сфере (геодистанция/Haversine) |
| GET    | `/organizations/in-rect?lat_min=…&lat_max=…&lon_min=…&lon_max=…` | Организации в заданной прямоугольной области |

>Протестировать можно через Swagger UI или ReDoc (ссылки выше).
