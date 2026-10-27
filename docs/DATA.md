# Dane katalogowe

Repozytorium nie zawiera wygenerowanego katalogu modeli. Skrypt `database/download_hotwheels.py` pobiera strony przez publiczne MediaWiki API Hot Wheels Wiki i zapisuje lokalny plik JSON. Importer `backend/import_hotwheels.py` przekształca wpisy na rekordy `cars` oraz `variants`.

## Pobieranie

Wymagania skryptu instalowane są z `database/requirements.txt`.

```bash
cd database
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python download_hotwheels.py
```

Skrypt przegląda strony wiki i wydobywa pola z infoboxów. Żądania sieciowe mogą długo trwać, a format strony źródłowej może się zmienić. Sprawdź wynik JSON przed importem. Nazwa oczekiwana przez importer to `database/hotwheels_models_new2.json`.

## Import

Najpierw skonfiguruj `DATABASE_URL` w `backend/.env`, a następnie:

```bash
cd backend
source .venv/bin/activate
python import_hotwheels.py --dry-run
python import_hotwheels.py
```

Tryb `--dry-run` raportuje liczbę rekordów i wariantów do dodania. Importer pomija warianty, które już istnieją według samochodu, numeru zabawki, roku, serii i koloru. Import wykonuje zapisy partiami; przed ponownym importem dużego zbioru wykonaj kopię zapasową bazy.

## Pola

Wariant może zawierać `toy_number`, `release_year`, `series_name`, `series_position`, `series_total`, `body_color`, `tampo`, `wheel_type`, `base_color`, `window_color`, `interior_color`, a także flagi Treasure Hunt. Opis wariantu jest budowany z dostępnych informacji o kolorze, tampo, kołach i ekskluzywności.

Numery zabawki są normalizowane do wielkich liter i bez spacji. Wartość w formacie `238/250` jest traktowana jako pozycja i liczba elementów serii, a nie numer zabawki.

## Warunki korzystania

Dane pochodzą z zewnętrznej wiki i mogą podlegać jej licencji oraz warunkom korzystania. Użytkownik odpowiada za ich sprawdzenie przed dalszą redystrybucją. Nie publikuj wygenerowanych plików bez oceny ich praw i pochodzenia.
