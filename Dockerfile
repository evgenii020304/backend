FROM python:3.9-slim

WORKDIR /app

# Копируем зависимости и устанавливаем их
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код backend
COPY backend/app.py .

# Создаем директорию для данных
RUN touch data.txt

# Открываем порт
EXPOSE 8000

# Запускаем приложение
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]