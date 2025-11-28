FROM python:3.9-slim

WORKDIR /app

# Копируем зависимости и устанавливаем их
RUN pip install --no-cache-dir \
    fastapi==0.115.0 \
    uvicorn[standard]==0.30.6 \
    pydantic==2.9.2

# Копируем исходный код backend
COPY . .

# Создаем директорию для данных
RUN touch data.txt

# Открываем порт
EXPOSE 8000

# Запускаем приложение
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]