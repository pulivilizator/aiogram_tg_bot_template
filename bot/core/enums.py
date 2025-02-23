from enum import StrEnum


class Languages(StrEnum):
    RU = "ru"
    EN = "en"

    WIDGET_KEY = "language"


class CacheLoadModules(StrEnum):
    SETTINGS = "settings"
