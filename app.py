from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import os

app = FastAPI(title="DevOps Backend", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_FILE = 'data.txt'

class SaveRequest(BaseModel):
    data: str

class SaveResponse(BaseModel):
    message: str
    timestamp: str
    savedData: str

class DataResponse(BaseModel):
    content: str
    isEmpty: bool

def ensure_data_file():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            f.write('')
        print(f"Файл {DATA_FILE} создан")

def get_last_line() -> str:
    try:
        if not os.path.exists(DATA_FILE):
            return None

        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        non_empty_lines = [line.strip() for line in lines if line.strip()]
        return non_empty_lines[-1] if non_empty_lines else None

    except Exception as e:
        print(f" Ошибка чтения файла: {e}")
        return None

@app.post("/save", response_model=SaveResponse)
async def save_data(request: SaveRequest):
    try:
        if not request.data or not request.data.strip():
            raise HTTPException(status_code=400, detail="Данные не предоставлены")

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        entry = f"[{timestamp}] {request.data}\n"

        with open(DATA_FILE, 'a', encoding='utf-8') as f:
            f.write(entry)

        print(f"Данные сохранены: {request.data}")
        return SaveResponse(
            message="Данные успешно сохранены",
            timestamp=timestamp,
            savedData=request.data
        )

    except HTTPException:
        raise
    except Exception as e:
        print(f" Ошибка сохранения: {e}")
        raise HTTPException(status_code=500, detail="Ошибка сохранения")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)