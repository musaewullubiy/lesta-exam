# Lesta Exam Project

Backend API для экзаменационного проекта, построенный на Flask с PostgreSQL в качестве базы данных. Проект контейнеризирован с помощью Docker и автоматизирован через Jenkins CI/CD.

## 🛠 Технологии
- **Backend**: Flask (Python 3.10)
- **База данных**: PostgreSQL
- **Контейнеризация**: Docker, Docker Compose
- **CI/CD**: Jenkins

## 📂 Структура проекта
```
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   └── schemas.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── .gitignore
├── Jenkinsfile
└── README.md
```

## 🚀 Установка и запуск (локально)

### Требования
- Docker и Docker Compose
- Python 3.10 (опционально, для разработки)
- Git

### Шаги
1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/musaewullubiy/lesta-exam.git
   cd lesta-exam
   ```

2. Настройте переменные окружения:
   ```bash
   cp .env.example .env
   ```
   Отредактируйте `.env` (пример):
   ```ini
   DB_USER=postgres
   DB_PASSWORD=your_secure_password
   DB_NAME=exam_db
   DB_HOST=db
   DB_PORT=5432
   ```

3. Запустите контейнеры:
   ```bash
   docker-compose up -d --build
   ```

4. Проверьте API:
   - **Пинг**:
     ```bash
     curl http://localhost:5000/ping
     ```
     Ожидаемый ответ: `{"status": "ok"}`

   - **Отправка результата**:
     ```bash
     curl -X POST http://localhost:5000/submit -H "Content-Type: application/json" -d '{"name": "Kirill", "score": 88}'
     ```
     Ожидаемый ответ: `{"message": "Submission recorded", "id": 1}`

   - **Получение результатов**:
     ```bash
     curl http://localhost:5000/results
     ```
     Ожидаемый ответ: `[{"id": 1, "name": "Kirill", "score": 88, "timestamp": "2025-06-08TXX:XX:XX"}]`

5. Остановите контейнеры:
   ```bash
   docker-compose down
   ```

## 🔄 CI/CD с Jenkins

### Настройка Jenkins
1. **Установите плагины**:
   - Docker Pipeline
   - SSH Agent

2. **Настройте SSH**:
   - Сгенерируйте SSH-ключ:
     ```bash
     ssh-keygen -t rsa -b 4096 -f ~/.ssh/jenkins_ssh_key
     ```
   - Скопируйте ключ на сервер:
     ```bash
     ssh-copy-id -i ~/.ssh/jenkins_ssh_key.pub ubuntu@your-remote-server-ip
     ```
   - Добавьте ключ в Jenkins через `Manage Jenkins > Manage Credentials`.

3. **Установите Docker**:
   ```bash
   sudo apt install docker.io docker-compose
   sudo usermod -aG docker Jenkins
   sudo systemctl restart Jenkins
   ```

4. **Создайте пайплайн**:
   - Тип: `Pipeline`
   - SCM: Git (`https://github.com/musaewullubiy/lesta-exam.git`)
   - Script Path: `Jenkinsfile`

### Настройка удаленного сервера
1. Установите Docker и Compose
2. Откройте порт:
   ```bash
   sudo ufw allow 5000
   ```
3. Проверьте деплой:
   ```bash
   curl http://your-remote-server-ip:5000/ping
   ```

## 🛠 Устранение неполадок
- **Host key verification failed**:
  ```bash
  sudo -u Jenkins -i ssh -i /var/lib/Jenkins/.ssh/jenkins_ssh_key ubuntu@your-remote-server-ip
  ```
  
- **Отсутствует .env**:
  Убедитесь, что файл `.env` создан на сервере через `Jenkinsfile`.

- **API не отвечает**:
  Проверьте логи:
  ```bash
  docker logs lesta-project_db_1
  ```
