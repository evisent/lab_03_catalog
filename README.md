# librarycatalog

Консольная утилита на Python: **каталог библиотечных книг** с сохранением в JSON.

## Возможности

- Добавление, получение и удаление книг по ID
- Поиск по категории и по названию (регистронезависимый)
- Детерминированный порядок итерации (по возрастанию ID)
- Сохранение и загрузка в JSON с `format_version`
- Загрузка без частичных изменений при повреждённом файле

## Установка

```bash
pip install -e .
```

## Использование

```bash
python -m librarycatalog add --file catalog.json --id 1 --title "War and Peace" --category fiction --year 1869 --author "Tolstoy" --isbn "978-5-04-116640-2"
python -m librarycatalog list --file catalog.json
python -m librarycatalog get --file catalog.json --id 1
python -m librarycatalog find --file catalog.json --name "war"
python -m librarycatalog remove --file catalog.json --id 1
```

## Структура

```
lab_03/
  pyproject.toml
  README.md
  .gitignore
  src/librarycatalog/
    __init__.py
    __main__.py
    models.py
    catalog.py
    storage.py
    errors.py
  tests/
    test_models.py
    test_catalog.py
    test_storage.py
```

## Тесты и линтер

```bash
python -m pytest
ruff check .
```