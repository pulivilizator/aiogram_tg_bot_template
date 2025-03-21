from fluent_compiler.bundle import FluentBundle
from fluentogram import FluentTranslator, TranslatorHub

DIR_PATH = "i18n/locales"


def i18n_factory() -> TranslatorHub:
    return TranslatorHub(
        locales_map={"ru": ("ru", "en"), "en": "en"},
        translators=[
            FluentTranslator(
                locale="ru",
                translator=FluentBundle.from_files(
                    locale="ru",
                    filenames=[f"{DIR_PATH}/ru/LC_MESSAGES/txt.ftl"],
                ),
            ),
            FluentTranslator(
                locale="en",
                translator=FluentBundle.from_files(
                    locale="en",
                    filenames=[f"{DIR_PATH}/en/LC_MESSAGES/txt.ftl"],
                ),
            ),
        ],
        root_locale="en",
    )
