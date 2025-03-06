from typing import TYPE_CHECKING, Any

from aiogram_dialog import DialogManager
from fluentogram import TranslatorRunner

from bot.core.enums import Languages

if TYPE_CHECKING:
    from i18n.stub import TranslatorRunner


async def menu_getter(
    dialog_manager: DialogManager,
    i18n: TranslatorRunner,
    **kwargs: Any,
) -> dict[str, Any]:
    return {
        "start_message": i18n.main_menu.start_message(),
        "languages": ((Languages.RU, i18n.lang.ru()), (Languages.EN, i18n.lang.en())),
    }
