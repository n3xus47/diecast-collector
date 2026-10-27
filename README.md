# Diecast Collector

> **Status: projekt porzucony.** Rozwój i utrzymanie aplikacji zostały zakończone. Repozytorium pozostaje publiczne jako archiwum kodu; nie należy oczekiwać poprawek, aktualizacji zależności ani wsparcia.

Diecast Collector to prototyp aplikacji do katalogowania modeli samochodów diecast. Mobilny klient Flutter pozwala przeglądać kolekcję i wyszukiwać modele po numerze. API w FastAPI przechowuje dane w PostgreSQL.

## Funkcje

- podgląd elementów kolekcji i daty ich dodania;
- identyfikacja modeli po numerze zabawki lub nazwie;
- wybór wariantu na podstawie roku, serii, koloru i numeru w serii;
- ręczne wyszukiwanie modelu po numerze z opakowania;
- pobieranie i import katalogu modeli z Hot Wheels Wiki.

## Technologie

- **Aplikacja:** Flutter i Dart, pakiet `http`;
- **API:** Python 3.10+, FastAPI, SQLModel, SQLAlchemy, Alembic;
- **Baza:** PostgreSQL;
- **Źródło danych:** MediaWiki API Hot Wheels Wiki.

## Struktura repozytorium

```text
backend/
  app/
    routers/       Endpointy wyszukiwania i kolekcji
    matching.py    Normalizacja i dopasowywanie wariantów
    models.py      Modele SQLModel, schematy API i połączenie z bazą
    main.py        Konfiguracja aplikacji FastAPI
  import_hotwheels.py
  requirements.txt
database/
  download_hotwheels.py
  requirements.txt
frontend/
  lib/             Aplikacja Flutter
docs/
  API.md
  ARCHITECTURE.md
  DATA.md
  DEVELOPMENT.md
```

## Wymagania

- Python 3.10 lub nowszy;
- PostgreSQL 13 lub nowszy;
- Flutter SDK zgodny z zakresem `>=3.0.0 <4.0.0` z `frontend/pubspec.yaml`;
- Android Studio/Android SDK dla Androida albo Xcode dla iOS;

## Szybki start

Instrukcja krok po kroku znajduje się w [QUICKSTART.md](QUICKSTART.md). W skrócie:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp ../.env.example .env
# Ustaw DATABASE_URL w pliku .env.
uvicorn app.main:app --reload
```

API startuje pod `http://localhost:8000`; dokumentacja OpenAPI jest dostępna pod `/docs`. Tabele są tworzone przy starcie aplikacji. Szczegóły konfiguracji i uruchomienia klienta mobilnego opisuje [przewodnik deweloperski](docs/DEVELOPMENT.md).

## Dokumentacja

- [Szybki start](QUICKSTART.md)
- [Endpointy API](docs/API.md)
- [Architektura](docs/ARCHITECTURE.md)
- [Dane i importer](docs/DATA.md)
- [Uruchamianie i konfiguracja](docs/DEVELOPMENT.md)

## Ograniczenia i bezpieczeństwo

Projekt jest prototypem, a nie usługą gotową do wdrożenia. API nie ma uwierzytelniania, więc wszystkie urządzenia korzystające z jednego backendu widzą tę samą kolekcję. CORS zezwala na zapytania z dowolnego źródła. Nie wystawiaj API do publicznego internetu ani nie przechowuj w nim wrażliwych danych.

Baza modeli wymaga osobnego pobrania i importu; w repozytorium nie ma gotowego zrzutu danych.

## Współtworzenie

Projekt nie jest aktywnie rozwijany i nie przyjmuje zgłoszeń o wsparcie. Kod można analizować i uruchamiać na własne ryzyko. Przed wykorzystaniem należy sprawdzić licencje zależności oraz warunki korzystania z danych Hot Wheels Wiki.

## Licencja

Repozytorium nie zawiera pliku licencji. Oznacza to, że nie udzielono tu ogólnej licencji na kopiowanie, modyfikowanie ani redystrybucję kodu. Zależności i dane zewnętrzne podlegają własnym warunkom.
