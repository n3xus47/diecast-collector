# API

API FastAPI domyślnie działa pod `http://localhost:8000`. Interaktywny opis OpenAPI jest dostępny pod `/docs`, a schemat JSON pod `/openapi.json`. Wszystkie identyfikatory rekordów są UUID. Daty zwracane przez API są zapisane w ISO 8601.

API nie uwierzytelnia użytkowników. Kolekcja jest wspólna dla wszystkich klientów podłączonych do danej bazy.

## `GET /`

Kontrola działania API.

```json
{"message":"Diecast Collector API"}
```

## `GET /identify/{code}`

Wyszukuje warianty po `toy_number`. Kod jest normalizowany do wielkich liter i może zawierać sufiks po łączniku. Opcjonalne parametry cech pomagają wybrać wariant.

| Parametr | Typ | Opis |
| --- | --- | --- |
| `year` | integer | Rok wydania |
| `series` | string | Nazwa serii |
| `color` | string | Kolor nadwozia |
| `series_number` | string | Pozycja w serii, np. `238/250` |

Przykład: `GET /identify/HYW54?year=2025&series_number=238%2F250`.

Odpowiedź zawiera `car` z polami `id`, `model_name`, `page_title` i listą `variants`. Brak pasującego kodu zwraca `404`.

## `GET /identify/by-name`

Wyszukuje nazwę samochodu lub tytuł strony.

| Parametr | Typ | Opis |
| --- | --- | --- |
| `model_name` | string | Wymagany fragment nazwy |
| `year`, `series`, `color`, `series_number` | różne | Opcjonalne wskazówki do wyboru wariantu, takie jak w `/identify/{code}` |

Pusta nazwa zwraca `400`; brak wyników zwraca `404`.

## `GET /cars/search`

Zwraca listę samochodów pasujących do fragmentu `model_name`, posortowaną według nazwy.

| Parametr | Typ | Domyślnie | Opis |
| --- | --- | --- | --- |
| `model_name` | string | — | Wymagany fragment nazwy |
| `limit` | integer | `50` | Maksymalna liczba wyników |
| `offset` | integer | `0` | Liczba pomijanych rekordów |

Każdy element zawiera samochód wraz z wariantami.

## `POST /collection`

Dodaje wariant do wspólnej kolekcji. Treść żądania:

```json
{"variant_id":"00000000-0000-0000-0000-000000000000"}
```

Zwraca element kolekcji z wariantem, samochodem i `added_at`. Jeśli wariant już istnieje w kolekcji, API zwraca istniejący wpis. Nieznany wariant zwraca `404`.

## `GET /collection`

Zwraca kolekcję od najnowszego wpisu.

| Parametr | Typ | Domyślnie | Opis |
| --- | --- | --- | --- |
| `limit` | integer | `200` | Maksymalna liczba elementów |
| `offset` | integer | `0` | Liczba pomijanych elementów |

## Model wariantu

Wariant zawiera identyfikator, `car_id`, `toy_number`, opis `desc`, flagi `is_chase`, `treasure_hunt`, `super_treasure_hunt` oraz dostępne cechy: rok, serię, pozycję i łączną liczbę w serii, kolor nadwozia, tampo i typ kół. Model bazy zawiera dodatkowo kolory bazy, szyb i wnętrza.
