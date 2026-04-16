LOCALE_ALIASES = {
    "ar": "ar",
    "de": "de",
    "en": "en-us",
    "en-in": "en-in",
    "es": "es",
    "fr": "fr",
    "hi": "hi",
    "id": "id",
    "it": "it-it",
    "it-it": "it-it",
    "ko": "kr",
    "kr": "kr",
    "ml": "ml-in",
    "ml-in": "ml-in",
    "ms": "bm-ms",
    "nl": "nl",
    "pl": "pl",
    "pt": "pt-br",
    "pt-br": "pt-br",
    "ru": "ru",
    "sv": "sv-se",
    "sv-se": "sv-se",
    "tr": "tr-tr",
    "tr-tr": "tr-tr",
    "uk": "uk",
    "ur": "ur-en",
    "ur-en": "ur-en",
    "zh": "zh-hant-tw",
    "zh-cn": "zh-hant-tw",
    "zh-hans": "zh-hant-tw",
    "zh-hk": "zh-hant-tw",
    "zh-tw": "zh-hant-tw",
    "zh-hant": "zh-hant-tw",
    "zh-hant-tw": "zh-hant-tw",
}


def normalize_locale(locale):
    if not locale:
        return "en-us"

    normalized = locale.strip().lower().replace("_", "-")
    if normalized in LOCALE_ALIASES:
        return LOCALE_ALIASES[normalized]

    base = normalized.split("-")[0]
    return LOCALE_ALIASES.get(base, "en-us")
