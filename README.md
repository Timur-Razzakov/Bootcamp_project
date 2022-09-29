## Описание проекта

Сервис по Рассылке нотификаций

### Стек технологий

- Django
- schedule
- PostgresSQL
- Jinja2
- Request
---
### Установка

Установливаем зависимости.

```
pip install -r requirements.txt
```

Миграции

```
python manage.py migrate
```

Загрузка Данных из Json файла

```
python manage.py loaddata < dumped_data.json
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
