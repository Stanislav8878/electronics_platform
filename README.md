# Electronics Platform

Веб-приложение для управления сетью по продаже электроники.  
Проект реализован на **Django**, **Django REST Framework**, **PostgreSQL** и **Docker**.

## Что реализовано

### 1. Модель сети электроники
Сеть представлена единой моделью `NetworkNode`, которая поддерживает три типа звеньев:

- завод;
- розничная сеть;
- индивидуальный предприниматель.

У каждого звена есть:

- название;
- email;
- страна;
- город;
- улица;
- номер дома;
- поставщик;
- задолженность перед поставщиком;
- дата создания.

Уровень иерархии рассчитывается автоматически по цепочке поставщиков, а не по названию звена.

### 2. Модель продуктов
Для каждого звена можно хранить продукты:

- название;
- модель;
- дата выхода на рынок.

### 3. Админ-панель
В административной панели реализовано:

- отображение созданных объектов;
- ссылка на поставщика на странице списка;
- фильтр по городу;
- admin action для очистки задолженности.

### 4. API
Реализован CRUD для звеньев сети и продуктов.

Основные маршруты:

- `/api/network/` — красивый предметный маршрут для сети;
- `/api/nodes/` — совместимый маршрут, оставлен для тестов;
- `/api/products/` — продукты;
- `/api/docs/` — Swagger UI;
- `/api/redoc/` — ReDoc.

### 5. Ограничения доступа
Доступ к API имеют только пользователи, которые одновременно:

- аутентифицированы;
- активны (`is_active=True`);
- являются сотрудниками (`is_staff=True`).

### 6. Ограничения бизнес-логики
Поддержаны проверки:

- завод не может иметь поставщика;
- узел не может ссылаться сам на себя;
- запрещены циклы в цепочке поставщиков;
- максимальная глубина иерархии — 3 уровня;
- поле задолженности нельзя менять через API при обновлении.

---

## Технологии

- Python 3.13
- Django 5.1.7
- Django REST Framework 3.15.2
- PostgreSQL 17
- Docker / Docker Compose
- drf-spectacular
- coverage

---

## Запуск проекта через Docker

### 1. Подготовка переменных окружения
Скопируйте файл `.env.example` в `.env`:

```bash
cp .env.example .env
```

Для Windows можно просто создать `.env` вручную на основе `.env.example`.

### 2. Сборка и запуск
```bash
docker compose up --build
```

После запуска приложение будет доступно по адресам:

- http://localhost:8000/admin/
- http://localhost:8000/api/nodes/
- http://localhost:8000/api/network/
- http://localhost:8000/api/products/
- http://localhost:8000/api/docs/
- http://localhost:8000/api/redoc/

### 3. Данные для входа в админку
По умолчанию суперпользователь создаётся автоматически из `.env`:

- логин: `admin`
- пароль: `admin12345`

---

## Запуск тестов

```bash
docker compose exec web python manage.py test
```

## Проверка покрытия

```bash
docker compose exec web coverage run manage.py test
docker compose exec web coverage report -m
```

Ожидаемый результат:

```text
TOTAL 100%
```

---

## Структура проекта

```text
electronics_platform/
├── config/
├── electronics/
│   ├── migrations/
│   ├── admin.py
│   ├── filters.py
│   ├── models.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── entrypoint.sh
├── manage.py
├── README.md
└── requirements.txt
```

---

## Проверка задания

### Админ-панель
- отображает объекты сети и продукты;
- показывает ссылку на поставщика;
- фильтрует узлы по городу;
- содержит action для очистки задолженности.

### API
- позволяет создавать, читать, изменять и удалять узлы;
- позволяет работать с продуктами;
- фильтрует узлы по стране;
- запрещает менять задолженность через API на обновлении.

### Тесты
Проект покрыт автоматическими тестами на 100%.

---

Name                                     Stmts   Miss  Cover   Missing
----------------------------------------------------------------------
config/__init__.py                           0      0   100%
config/settings.py                          23      0   100%
config/urls.py                               4      0   100%
electronics/__init__.py                      0      0   100%
electronics/admin.py                        27      0   100%
electronics/apps.py                          4      0   100%
electronics/filters.py                       7      0   100%
electronics/migrations/0001_initial.py       7      0   100%
electronics/migrations/__init__.py           0      0   100%
electronics/models.py                       55      0   100%
electronics/permissions.py                   5      0   100%
electronics/serializers.py                  16      0   100%
electronics/tests.py                       123      0   100%
electronics/urls.py                          9      0   100%
electronics/views.py                        16      0   100%
manage.py                                    7      0   100%
----------------------------------------------------------------------
TOTAL                                      303      0   100%
