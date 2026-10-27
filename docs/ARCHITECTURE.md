# Architektura

Diecast Collector składa się z aplikacji mobilnej Flutter, API FastAPI i relacyjnej bazy PostgreSQL. Klient wysyła żądania HTTP do API; API odczytuje modele i warianty z bazy oraz zapisuje wpisy kolekcji.

```text
frontend/lib/
  screens/          Widok kolekcji i formularz dodawania modelu
  services/         Klient HTTP API
  models/           Modele JSON po stronie Fluttera

backend/app/
  main.py            Konfiguracja FastAPI, CORS i routerów
  routers/cars.py    Wyszukiwanie i identyfikacja modeli
  routers/collection.py Operacje na kolekcji
  matching.py        Normalizacja i ocena podobieństwa wariantów
  models.py          Silnik bazy, SQLModel i schematy odpowiedzi

database/
  download_hotwheels.py  Pobieranie stron z MediaWiki API
backend/import_hotwheels.py  Import JSON do bazy
```

## Dodawanie modelu

1. Użytkownik wpisuje numer modelu z opakowania.
2. Aplikacja wysyła numer do `GET /identify/{code}`.
3. API zwraca samochód i warianty.
4. Po wyborze wariantu klient wysyła jego UUID do `POST /collection`.

## Model danych

- `cars` przechowuje nazwę modelu oraz tytuł strony źródłowej;
- `variants` przechowuje numer zabawki, cechy wydania i relację do samochodu;
- `user_collection` wskazuje wybrany wariant i czas dodania.

Każdy wpis kolekcji ma relację do wariantu, a wariant do samochodu. Aplikacja tworzy brakujące tabele przy uruchomieniu. W `models.py` pozostaje zgodność migracyjna dla wybranych starszych kolumn; repozytorium zawiera konfigurację Alembic, ale obecny start aplikacji nie wykonuje `alembic upgrade`.

## Granice prototypu

W bazie nie ma użytkowników ani izolacji kolekcji, API nie ma uwierzytelniania, a CORS dopuszcza dowolne źródło. Przed wdrożeniem wymagane byłyby co najmniej uwierzytelnianie, model własności kolekcji, kontrola pochodzenia żądań, migracje i ograniczenia dostępu do bazy. Projekt nie jest obecnie rozwijany.
