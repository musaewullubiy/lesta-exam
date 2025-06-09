Lesta Exam

Backend: Flask (Python 3.10)
База данных: PostgreSQL
Контейнеризация: Docker, Docker Compose
CI/CD: Jenkins

Структура проекта
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


app/: Код Flask-приложения.
Dockerfile: Инструкции для сборки Docker-образа.
docker-compose.yml: Конфигурация для запуска API и PostgreSQL.
requirements.txt: Зависимости Python.
.env.example: Шаблон переменных окружения.
Jenkinsfile: Пайплайн для CI/CD.
.gitignore: Игнорируемые файлы.

Установка и запуск локально
Требования

Docker и Docker Compose
Python 3.10 (опционально, для разработки)
Git

Шаги

Клонируйте репозиторий:
git clone https://github.com/musaewullubiy/lesta-exam.git
cd lesta-exam


Создайте файл .env:Скопируйте .env.example в .env и задайте переменные:
cp .env.example .env

Пример .env:
DB_USER=postgres
DB_PASSWORD=your_secure_password
DB_NAME=exam_db
DB_HOST=db
DB_PORT=5432


Запустите контейнеры:
docker-compose up -d --build

Проверьте API:

Пинг:curl http://localhost:5000/ping

Ожидаемый ответ: {"status": "ok"}
Отправка результата:curl -X POST http://localhost:5000/submit -H "Content-Type: application/json" -d '{"name": "Kirill", "score": 88}'

Ожидаемый ответ: {"message": "Submission recorded", "id": 1}
Получение результатов:curl http://localhost:5000/results

Ожидаемый ответ: [{"id": 1, "name": "Kirill", "score": 88, "timestamp": "2025-06-08TXX:XX:XX"}]


Остановите контейнеры:
docker-compose down



CI/CD с Jenkins
Проект использует Jenkins для автоматизации сборки и деплоя на удаленный сервер.
Настройка Jenkins

Установите плагины:

В Jenkins: ManageJenkins > ManageJenkins > Plugins > AvailableAvailable.
Установите: Docker Pipeline, SSH Agent.


Настройте SSH:

Сгенерируйте SSH-ключ:ssh-keygen -t rsa -b 4096 -f ~/.ssh/jenkins_ssh_key

Скопируйте ключ на удаленный сервер:ssh-copy-id -i ~/.ssh/jenkins_ssh_key.pub ubuntu@your-remote-server-ip


Добавьте ключ в Jenkins:
Manage Jenkins > Manage Credentials > (global) > Add Credentials.
Kind: SSH Username with private key.
ID: remote-ssh-credentials.
Username: ubuntu.
Private Key: Вставьте содержимое ~/.ssh/jenkins_ssh_key.


Установите Docker и Compose:
sudo apt install docker.io docker-compose
sudo usermod -aG docker Jenkins
sudo systemctl restart Jenkins


Создайте пайплайн:
В Jenkins: New Item > Pipeline.
Имя: lesta-project.
Поставьте галочку This project is parameterized:
REMOTE_HOST: IP удаленного сервера.
REMOTE_USER: Пользователь.
REMOTE_DIR: Директория проекта.


Pipeline: Pipeline script from SCM.
SCM: Git.
URL: https://github.com/musaewullubiy/lesta-exam.git.
Branch: master.
Script Path: Jenkinsfile.


Запустите пайплайн:
Build with Parameters > Укажите параметры > Build.

Настройка удаленного сервера
Установите Docker и Compose

Откройте порт 5000:
sudo ufw allow 5000

Проверьте деплой:
cd /home/ubuntu/EXAM
docker ps
curl http://your-remote-server-ip:5000/ping

Устранение неполадок

Jenkins: Host key verification failed:
Под пользователем Jenkins добавьте хост:sudo -u Jenkins -i
ssh -i /var/lib/Jenkins/.ssh/jenkins_ssh_key ubuntu@your-remote-server-ip

Скопируйте ключ:sudo cp ~/.ssh/jenkins_ssh_key /var/lib/Jenkins/.ssh/
sudo chown Jenkins:Jenkins /var/lib/Jenkins/.ssh -R


Отсутствует .env:
Проверьте .env.example в репозитории.
Убедитесь, что .env создается на сервере через Jenkinsfile.


API не отвечает:
Проверьте логи базы данных:docker logs lesta-project_db_1
