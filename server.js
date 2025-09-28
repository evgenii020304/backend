import express from 'express';
import fs from 'fs';
import path from 'path';
import cors from 'cors';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const PORT = 3000;

app.use(cors());
app.use(express.json());

const ensureDataFileExists = () => {
    const filePath = path.join(__dirname, 'data.txt');
    if (!fs.existsSync(filePath)) {
        fs.writeFileSync(filePath, '');
        console.log('Файл data.txt создан');
    }
};

const getLastLine = () => {
    try {
        const filePath = path.join(__dirname, 'data.txt');
        if (!fs.existsSync(filePath)) {
            return null;
        }

        const data = fs.readFileSync(filePath, 'utf8');
        const lines = data.split('\n').filter(line => line.trim());
        return lines.length > 0 ? lines[lines.length - 1] : null;
    } catch (error) {
        console.error('Ошибка чтения файла:', error);
        return null;
    }
};

app.post('/save', (req, res) => {
    const {data} = req.body;

    if(!data) {
        return res.status(400).json({error: 'Данные не предоставлены'});
    }

    const timestamp = new Date().toLocaleString('ru-RU');
    const entry = `[${timestamp}] ${data}\n`;

    fs.appendFile('data.txt', entry, (err) => {
        if(err) {
            console.error('Ошибка записи:', err);
            return res.status(500).json({error: 'Ошибка сохранения'});
        }
        console.log('Данные сохранены:', data);
        res.json({message: 'Данные успешно сохранены', timestamp});
    });
});

app.get('/data', (req, res) => {

    const lastLine = getLastLine();

    if (!lastLine) {
        console.log('Файл пуст');
        return res.json({
            content: 'Файл data.txt пуст',
            isEmpty: true
        });
    }

    console.log('Последние данные:', lastLine);
    res.json({
        content: lastLine,
        isEmpty: false
    });
});

app.listen(PORT, () => {
    ensureDataFileExists();
    console.log(`✅ Backend сервер запущен на http://localhost:${PORT}`);
    console.log(`📁 Файл данных: ${path.join(__dirname, 'data.txt')}`);
});