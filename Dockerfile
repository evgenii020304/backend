# образ Python
FROM python:3.11-slim

# Рабочая директория
WORKDIR /app

# Устанавливаем зависимости
RUN pip install --no-cache-dir \
    fastapi==0.115.0 \
    uvicorn[standard]==0.30.6 \
    pydantic==2.9.2

# Копируем файлы
COPY . .

# Открываем порт
EXPOSE 8000

# Запускаем сервер
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]