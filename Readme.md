#### Python 3.12.2

### Poetry
```Bash
# Создание requirements.txt экспорта зависимостей без хэшей
poetry export --without-hashes -f requirements.txt --output requirements.txt  

# или аналогичная команда
poetry export --without-hashes --format=requirements_dev.txt > requirements_dev.txt
```

### Delete all in docker
```bash
docker system prune -af
```

### download all packages for local install 
```bash
pip download -d vendor -r requirements.txt
```

### Install all packages localhost from folder
```bash
pip install --no-index --find-links /vendor -r requirements.txt
```
- (install wheel package) https://stackoverflow.com/questions/51748058/all-dependencies-are-not-downloaded-with-pip-download


mklink /D "D:\Python\file_observer\data" "\\10.5.3.48\Архив\Отдел информационных технологий\2. Общая\01---kdedov"
