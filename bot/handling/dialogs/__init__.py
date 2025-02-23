from aiogram_dialog import Dialog

from .main_menu import dialog as menu_dialog

def get_dialogs() -> list[Dialog]:
    return [
        menu_dialog,
    ]