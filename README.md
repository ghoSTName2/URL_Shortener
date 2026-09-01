Технології:
    Python
    FastAPI
    SQLalchemy

Структура проекту:

    URL_Shortener/
        database.py - +
        models.py - + 
        schemas.py - +
        utils.py - +
        shortener.py
        routers/
            shortener.py
        main.py

Структура моделі:

    UrlShortener:
        id — унікальний ідентифікатор (ціле число або UUID).
        short_code — короткий унікальний рядок (наприклад, x7K9a). Повинен бути індексованим для швидкого пошуку.
        original_url — оригінальне довге посилання (рядок).
        clicks — лічильник переходів (ціле число, за замовчуванням 0).
        created_at — дата та час створення.
        last_clicked_at — дата та час останнього переходу (може бути None спочатку).


Стандартний Respones:
    {
        "code": "x7K9a",
        "original_url": "https://www.google.com/maps/...",
        "clicks": 42,
        "last_clicked_at": "2026-08-29T17:28:00"
    }   