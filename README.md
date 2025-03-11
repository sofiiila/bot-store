[My public Repositories ------------------->](https://github.com/sofiiila/sofiiila/blob/main/content_table.md)

# BOT_STORE
#### Бот-сборщик заявок. 
#### - Сценарий опроса клиента.
#### - Сохранение заявки.
#### - Отправка заявок на CRM.
#### - Резервирование заявок.
#### - Удаление заявок только после ответа от CRM.

# Требования
#### Для запуска этого проекта необходимо установить Docker

# Начало работы
## Установка

```bash
#Клонировать репозиторий
git clone git@github.com:sofiiila/bot-store.git

# Перейдите в директрию проекта
cd bot_store
```
## Запуск контейнера локально

```bash
docker-compose -f docker-compose-local.yml up
```
## Запуск тестов

```bash
python test.py
```

## Проверка линтерами

```bash
mypy src

pylint src
```

## Схема бота

![Схема бота](СХЕМАБОТА.png)

## Status Badges
![Mypy Check](https://github.com/sofiiila/bot-store/actions/workflows/CI_pipeline.yml/badge.svg?branch=dev_0.0/gl-autodeploy&job=mypy-check)
![Pylint Check Status](https://github.com/sofiiila/bot-store/actions/workflows/CI_pipeline.yml/badge.svg?branch=dev_0.0/gl-autodeploy&job=pylint-check)
