# Hifenator

Web aplikacija za hifenaciju tekstova na srpskom jeziku u .docx formatu

## Potrebne stvari

Za backend:
 * Python 3.9+
 * Django
 * Gunicorn
 * SQLite

Za frontend:
 * Angular 13
 * PrimeNG 13

## Podešavanje za razvoj

Kreiranje virtuelnog okruženja:
```bash
cd backend
python3 -m venv .env
source .env/bin/activate
pip install -r requirements.txt
./manage.py migrate
```

Pokretanje testova:
```bash
python manage.py test
```

Pokretanje razvojnog servera:
```bash
./manage.py runserver
./manage.py qcluster
```

Pokretanje frontend servera iz korenskog direktorijuma Angular
projekta, dakle `korpus/frontend`:
```bash
ng serve
```

## Pravljenje Docker slike

Iz osnovnog foldera:
```
docker-compose build
docker-compose up -d
```

## Produkcija
```
mkdir /var/apps
cd /var/apps
git clone https://github.com/mbranko/hifenator.git
cd hifenator
mkdir log
mkdir media
docker-compose build
docker network create hifenator
docker network add hifenator traefik
docker-compose up -d
```
