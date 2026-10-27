"""Normalizacja identyfikatorów i dopasowywanie cech wariantów."""

import re
from difflib import SequenceMatcher
from typing import Optional, Set

def normalize_toy_number(toy_number: str) -> str:
    """
    Normalizuj toy_number - spójna normalizacja używana w całym systemie.
    Format: uppercase + strip + remove spaces
    """
    if not toy_number:
        return ""
    return str(toy_number).strip().upper().replace(' ', '')

def parse_release_year(year_value) -> Optional[int]:
    """
    Parsuj release_year z różnych formatów do int.
    Obsługuje: int, string z liczbą, zakresy (np. "2021 - present" -> 2021)
    """
    if year_value is None:
        return None

    if isinstance(year_value, int):
        return year_value

    year_str = str(year_value).strip()
    if not year_str:
        return None

    if ' - ' in year_str or '–' in year_str or ' to ' in year_str.lower():
        year_match = re.search(r'(\d{4})', year_str)
        if year_match:
            try:
                return int(year_match.group(1))
            except (ValueError, TypeError):
                return None

    try:
        return int(year_str)
    except (ValueError, TypeError):
        return None

def clean_series_name(series_name: Optional[str]) -> Optional[str]:
    """
    Czyści series_name z końcowych cyfr i znaków typu "4/5", "24/100".
    Przykłady:
    - "Hot Wheels Monster Trucks: Teenage Mutant Ninja Turtles4/5" -> "Hot Wheels Monster Trucks: Teenage Mutant Ninja Turtles"
    - "2004 First Editions24/100" -> "2004 First Editions"
    """
    if not series_name:
        return None

    cleaned = re.sub(r'\d+/\d+$', '', series_name)
    cleaned = re.sub(r'\d+$', '', cleaned)
    cleaned = cleaned.strip()

    return cleaned if cleaned else series_name

def normalize_color_tokens(color: str) -> Set[str]:
    """
    Normalize color names to a small base palette for fuzzy matching.
    """
    if not color:
        return set()

    text = re.sub(r'[^a-z0-9]+', ' ', color.lower()).strip()
    tokens = text.split()
    tokens = ["gray" if t == "grey" else t for t in tokens]

    base_colors = {
        "black", "white", "red", "blue", "green", "yellow", "orange",
        "purple", "pink", "gold", "silver", "gray", "brown", "tan",
        "bronze", "chrome"
    }
    return {t for t in tokens if t in base_colors}

def fuzzy_ratio(a: str, b: str) -> float:
    if not a or not b:
        return 0.0
    return SequenceMatcher(None, a, b).ratio()

def normalize_color_string(color: str) -> str:
    return re.sub(r'[^a-z0-9]+', ' ', color.lower()).strip()

def parse_series_number(series_number_str: Optional[str]) -> tuple[Optional[int], Optional[int]]:
    """
    Parsuj series_number z formatu "238/250" do (series_position, series_total).
    Zwraca (None, None) jeśli nie można sparsować.
    """
    if not series_number_str:
        return (None, None)

    if '/' not in str(series_number_str):
        return (None, None)

    try:
        parts = str(series_number_str).split('/')
        if len(parts) == 2:
            position = int(parts[0].strip())
            total = int(parts[1].strip())
            return (position, total)
    except (ValueError, IndexError):
        pass

    return (None, None)

def match_variant_by_features(variants, year, series, color, series_position=None, series_total=None):
    """
    Dopasuj wariant na podstawie dostępnych cech.

    Args:
        variants: Lista wariantów do dopasowania
        year: release_year
        series: series_name
        color: body_color
        series_position: Pozycja w serii
        series_total: Całkowita liczba w serii
    """
    if not variants:
        return None

    best_match = None
    best_score = 0

    for variant in variants:
        score = 0
        matches = 0

        if year is not None and variant.release_year is not None:
            if year == variant.release_year:
                score += 0.3
                matches += 1

        if series and variant.series_name:
            series_cleaned = clean_series_name(series)
            variant_series_cleaned = clean_series_name(variant.series_name)
            if series_cleaned and variant_series_cleaned:
                series_lower = series_cleaned.lower().strip()
                variant_series_lower = variant_series_cleaned.lower().strip()
                if series_lower in variant_series_lower or variant_series_lower in series_lower:
                    score += 0.25
                    matches += 1

        if color and variant.body_color:
            color_lower = color.lower().strip()
            variant_color_lower = variant.body_color.lower().strip()
            if color_lower in variant_color_lower or variant_color_lower in color_lower:
                score += 0.2
                matches += 1
            else:
                color_tokens = normalize_color_tokens(color_lower)
                variant_tokens = normalize_color_tokens(variant_color_lower)
                if color_tokens and variant_tokens and color_tokens.intersection(variant_tokens):
                    score += 0.12
                    matches += 1
                else:
                    similarity = fuzzy_ratio(
                        normalize_color_string(color_lower),
                        normalize_color_string(variant_color_lower)
                    )
                    if similarity >= 0.8:
                        score += 0.08
                        matches += 1

        if series_position is not None and series_total is not None:
            if (variant.series_position == series_position and
                variant.series_total == series_total):
                score += 0.25
                matches += 1

        if score > best_score:
            best_score = score
            best_match = {'variant': variant, 'score': score, 'matches': matches}

    return best_match
