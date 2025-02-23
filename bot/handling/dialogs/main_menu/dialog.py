from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Row, Radio
from aiogram_dialog.widgets.text import Format

from bot.core.enums import Languages
from bot.handling.dialogs.main_menu.getters import menu_getter
from bot.handling.states.main_menu import MainMenuSG
from bot.handling.utils.button_checker import SetButtonChecked

dialog = Dialog(
    Window(
        Format('{start_message}'),
        Row(
            Radio(
                checked_text=Format('🔘 {item[1]}'),
                unchecked_text=Format('⚪️ {item[1]}'),
                id=Languages.WIDGET_KEY.value,
                item_id_getter=lambda x: x[0],
                items='languages',
            ),
        ),
        getter=menu_getter,
        state=MainMenuSG.menu
    ),
    on_start=SetButtonChecked(Languages)
)