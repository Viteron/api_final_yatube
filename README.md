### проект api_final:
```
Проект предназначен для публикации постов. В этих постах можно выражать свои мысли,
делиться интересными наблюдениями или вести свой дневник. 

```
### Как запустить проект api_final:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Viteron/api_final_yatube.git
```

```
cd api_final_yatube
```

Cоздать и активировать виртуальное окружение:

```
python -m venv venv
```

* Если у вас Linux/macOS

    ```
    source env/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

```
python -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```


### Примеры некоторых запросов к API:
Добавление новой публикации в коллекцию публикаций. 
http://127.0.0.1:8000/api/v1/posts/

```
{
  "text": "string",
  "image": "string",
  "group": 0
}
```

Получение публикации по id.
http://127.0.0.1:8000/api/v1/posts/{id}/

```
{
  "id": 0,
  "author": "string",
  "text": "string",
  "pub_date": "2019-08-24T14:15:22Z",
  "image": "string",
  "group": 0
}
```

Добавление нового комментария к публикации.
http://127.0.0.1:8000/api/v1/posts/{post_id}/comments/

```
{
  "text": "string"
}
```