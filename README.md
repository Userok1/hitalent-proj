# hitalent-proj
## Usage
Склонируйте репозиторий:
```bash
git clone https://github.com/Userok1/hitalent-proj.git
```
Затем перейдите в рабочий каталог:
```bash
cd hitalent-proj
```
В рабочей директории создайте .evn файл и скопируйте туда содержимое файла .env.example:
```bash
touch .env
cp .env.example .env
```
Откройте .env и заполните параметры соответствующими значениями, чтобы сформировать полный postgresql url
Далее выполните команду docker compose up для формирования контейнера приложения и его запуска:
```bash
docker compose up --build
```
Далее в браузере введите ссылку http://0.0.0.0:8000/docs и перейдите в нее.
