# Backend Test

[![GitHub license](https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square)](https://github.com/ILope92/SampleCode/blob/master/LICENSE)

Сделано и основано на [техническом задании](https://github.com/ILope92/backend_test/blob/master/docs/test_task.md)

## Оглавление

- [Описание проекта](#description)

  - [Endpoints](#endpoints)
  - [API документация](#api)

- [Развернуть приложение](#deploy)

  - [Docker-compose](#deploy)
  - [Миграция Alembic](#alembic)

- [Конфигурирование](#config)

  - [Основной конфиг для проекта](#configapp)
  - [Environment](#env)

- [Тестирование](#test)

<a name="description"></a>

## 1. Описание проекта

В основе, это лишь базовый набор для воссоздания более сложных проектов в дальнейшем. Архитектура подобного плана позволяет отлично расширять приложение, и работать с endpoints более модульно. Реализована вся базовая работа с docker, docker-compose, миграциями, тестами, и конфигурированием.

<hr>
<a name="endpoints"></a>

## 1.1 Endpoints

Конечные точки предоставляют данные в нужном его виде для различных целей. Данные в этом проекте тестовые и представляют собой набор пользователей.
В проекте реализовано два метода для работы с базой:

### Пользователи

- (GET) [/api/auth/users]() - Получение списка пользователей
- (POST) [/api/auth/users/create]() - Создание пользователя
- (POST) [/api/auth/users/register]() - Регистрация пользователя
- (GET) [/api/auth/users/get/me]() - Получения данных пользователя (себя)
- (PUT) [/api/auth/users/update/me]() - Обновление данных пользователя (себя)
- (GET) [/api/auth/users/get/{user_id}]() - Получить данные пользователя по id
- (PUT) [/api/auth/users/update/{user_id}]() - Обновление данных пользователя по id
- (DELETE) [/api/auth/users/delete/{user_id}]() - Обновление данных пользователя по id

### Авторизация

- (POST) [/api/auth/login/access-token]() - Авторизация пользователя с получением токена доступа

<hr>
<a name="api"></a>

## 2. API документация

- http://localhost:8000/api/docs
- http://localhost:8000/api/redocs

## 3. Развернуть приложение

<a name="deploy"></a>

### 3.1 Docker-compose

Для сборки локального варианта и запуска проекта используйте следующую команду:

```bash
~ docker-compose -f docker-compose.local.yaml up
```

Будут собраны и настроены для работы следующие контейнеры

- backend (application)
- db (postgres 12)

Для сборки варианта в production и запуска проекта используйте следующую команду:

```bash
~ docker-compose -f docker-compose.prod.yaml up
```

Будут собраны и настроены для работы следующие контейнеры

- nginx
- certbot
- pgadmin
- backend (application)
- db (postgres 12)

<hr>

### 3.2 Миграция Alembic

<a name="alembic"></a>
Следующая команда применит миграции alembic. Существует 2 файла миграции, 1-ый создаёт таблицу, 2-ой задаёт пользователя с правами.

```bash
~ docker-compose backend exec alembic upgrade head
```

<hr>
<a name="config"></a>

### 4. Конфигурирование

Описание возможных конфигураций и для чего это необходимо, будут описываться здесь, для более глубокого понимания проекта.
<a name="configapp"></a>

### 4.1 Основной конфиг для проекта

Основной файл настроек используемый внутри проекта находится здесь:

- ./app/settings/config.py

Там же есть уже готовые шаблоны для работы с несколькими вариантами проекта (prod и local).

### 4.2 Environment

<a name="env"></a>

Существует два файла, исходя из названия понятно их предназначение:

- .local.env - Для локальной разработки
- .prod.env - В продакшн

Используемые данные в этих файлах, выложены в качестве показа. В дальнейшем не планируйте выкладывать данные куда - либо.

<hr>
<a name="test"></a>

### 5. Тестирование

Выполнение тестов локально

```bash
~ python -m pytest
```

Выполнение тестов в контейнере

```bash
~ docker-compose exec backend cd ./app | python -m pytest
```

Тесты создают базу данных в существующем docker-контейнере, применяет первые миграции к ней, и тестирует endpoins
