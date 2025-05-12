import os
import re
from datetime import datetime
from fastapi import FastAPI, UploadFile, File, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.database import engine, get_db
from app import models, crud
from app.schemas import EDFDataResponse
import mne

models.Base.metadata.create_all(bind=engine)
app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

FILENAME_RE = re.compile(r"(?P<date>\d{4}-\d{2}-\d{2})_(?P<time>\d{2}\.\d{2})\.edf$")


# HTML форма и отображение результатов
@app.get("/upload-edf/", response_class=HTMLResponse)
async def upload_edf_form(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})


# Обработка загрузки файла
@app.post("/upload-edf/", response_class=HTMLResponse)
async def upload_edf(
    request: Request, file: UploadFile = File(...), db=Depends(get_db)
):
    error_message = None
    edf_data = None

    try:
        # Сохраняем файл
        temp_path = f"temp_{file.filename}"
        with open(temp_path, "wb") as f:
            f.write(await file.read())

        # Читаем EDF
        raw = mne.io.read_raw_edf(temp_path, preload=False)

        # Парсим имя файла
        base = os.path.splitext(file.filename)[0]
        date_part, time_part = base.split("_")
        timestamp = datetime.strptime(f"{date_part} {time_part}", "%Y-%m-%d %H.%M")

        # Формируем данные
        edf_data = {
            "filename": file.filename,
            "channel_count": len(raw.ch_names),
            "sampling_freq": raw.info["sfreq"],
            "duration": float(raw.times[-1]),
            "timestamp": timestamp,
        }

        # Сохраняем в БД
        crud.create_edf_data(db, edf_data)
        os.remove(temp_path)

    except Exception as e:
        error_message = f"Ошибка: {str(e)}"
        if os.path.exists(temp_path):
            os.remove(temp_path)

    return templates.TemplateResponse(
        "upload.html",
        {"request": request, "edf_data": edf_data, "error_message": error_message},
    )
