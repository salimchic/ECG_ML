## Описание
Микросервис для чтения файлов edf формата

## Запуск
```bash
docker-compose up --build
```
```bash
curl.exe -X POST -F file=@".\Data\01\2025-03-17_10.34.edf" http://localhost:8000/upload-edf/
```

## Использование
1. Перейдите на страницу загрузки: [http://localhost:8000/upload-edf/](http://localhost:8000/upload-edf/).
2. Выберите EDF-файл в формате.
3. После загрузки отобразятся данные файла.

## Пример интерфейса
![image](https://github.com/user-attachments/assets/4e2a37b5-83e3-4d77-94cd-11c312461a3d)
