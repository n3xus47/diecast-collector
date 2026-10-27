# Szybki start

Instrukcja uruchamia prototyp lokalnie. Do korzystania z aplikacji mobilnej wymagany jest działający backend i baza PostgreSQL.

## 1. Backend

Wymagane: Python 3.10+, PostgreSQL oraz utworzona baza danych.

```bash
createdb diecast_db
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp ../.env.example .env
```

W pliku `backend/.env` ustaw prawidłowy adres bazy:

```dotenv
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/diecast_db
```

Uruchom API z katalogu `backend`:

```bash
uvicorn app.main:app --reload
```

Sprawdź `http://localhost:8000/` oraz dokumentację `http://localhost:8000/docs`.

## 2. (Opcjonalnie) dane katalogowe

Pobierz dane z Hot Wheels Wiki i zaimportuj je do bazy. Pobieranie wymaga dostępu do internetu i może potrwać długo.

```bash
cd database
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python download_hotwheels.py
```

Importer oczekuje pliku `database/hotwheels_models_new2.json`:

```bash
cd ../backend
source .venv/bin/activate
python import_hotwheels.py --dry-run
python import_hotwheels.py
```

Pliki JSON są pomijane przez Git i nie są dostarczane z repozytorium. Więcej informacji: [docs/DATA.md](docs/DATA.md).

## 3. Aplikacja Flutter

Zainstaluj Flutter SDK, Android SDK lub Xcode, a następnie:

```bash
cd frontend
flutter pub get
flutter run --dart-define=API_BASE_URL=http://10.0.2.2:8000
```

`10.0.2.2` jest adresem hosta widzianym z emulatora Androida. Na iOS Simulator użyj zwykle `http://localhost:8000`; na fizycznym urządzeniu podaj adres IP komputera w tej samej sieci Wi-Fi, np. `http://192.168.1.20:8000`.

Aby dodać samochód, wybierz zakładkę „Add”, wpisz numer z opakowania i wybierz właściwy wariant.

## Dalsza dokumentacja

- [Endpointy i przykłady API](docs/API.md)
- [Konfiguracja środowiska](docs/DEVELOPMENT.md)
- [Baza i import danych](docs/DATA.md)

Projekt jest porzucony. Przed wdrożeniem uwzględnij ograniczenia opisane w [README](README.md#ograniczenia-i-bezpieczeństwo).
