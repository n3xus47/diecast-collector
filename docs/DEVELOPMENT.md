# Uruchamianie i konfiguracja

Projekt jest porzucony i zależności nie są aktywnie aktualizowane. Instrukcja opisuje lokalne uruchomienie, nie wdrożenie produkcyjne.

## Backend

Wymagane: Python 3.10+, PostgreSQL oraz baza `diecast_db`.

```bash
createdb diecast_db
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp ../.env.example .env
```

Edytuj `backend/.env`, ustawiając `DATABASE_URL`. Następnie uruchom:

```bash
uvicorn app.main:app --reload
```

Można też użyć `./run_server.sh`; skrypt uruchamia Uvicorn z `--reload`. Aplikacja tworzy tabele przy starcie. `/docs` udostępnia interaktywną dokumentację API.

## Aplikacja Flutter

Wymagane: Flutter SDK oraz narzędzia platformy docelowej.

```bash
cd frontend
flutter pub get
flutter run --dart-define=API_BASE_URL=http://10.0.2.2:8000
```

Adres `API_BASE_URL` należy ustawić dla środowiska uruchomieniowego. Android Emulator używa zwykle `10.0.2.2`, iOS Simulator `localhost`, a urządzenie fizyczne adresu IP komputera widocznego w lokalnej sieci. Backend musi nasłuchiwać na interfejsie osiągalnym z urządzenia, np. przez `uvicorn app.main:app --host 0.0.0.0`.

## Zależności

- `backend/requirements.txt` zawiera zależności API;
- `database/requirements.txt` zawiera zależności pobierania katalogu;
- `frontend/pubspec.yaml` i `frontend/pubspec.lock` opisują pakiety Fluttera.

Android SDK i narzędzia Flutter instaluj lokalnie zgodnie z oficjalną dokumentacją platform. Nie są częścią źródeł projektu.
