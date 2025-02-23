from typing import Literal

class TranslatorRunner:
    def get(self, path: str, **kwargs) -> str: ...

    main_menu: Main_menu
    lang: Lang

class Main_menu:
    @staticmethod
    def start_message() -> Literal[
        """&lt;b&gt;The main menu of the bot.&lt;/b&gt;"""
    ]: ...

class Lang:
    @staticmethod
    def ru() -> Literal["""🇷🇺 Русский"""]: ...
    @staticmethod
    def en() -> Literal["""🇬🇧 English"""]: ...
