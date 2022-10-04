# Nexign_bootcamp_project
## Описание проекта

Сервис по Рассылке нотификаций для стажировки в Nexign

### Стек технологий

- Django
- schedule
- PostgresSQL
- Jinja2
- RabbitMQ
---
### Данные суперпользователя

### Установка

Установливаем зависимости.

```
pip install -r requirements.txt
```

Выполним миграции

```
python manage.py migrate
```

Загрузка Данных из Json файла

```
python manage.py loaddata  dumped_data.json
```

Запуск скрипта, для заполнения формы "Result". Перейдите в директорию "cd result_create" 

```
python get_result.py
```

Запуск скриптов, для отправки по телеграмму и по почте.  Перейдите в директорию "cd sending_notifications"

```
python send_email.py
```

```
python send_to_tg.py
```

Запускаем проект на компьютере

```
python manage.py runserver 
```

---
