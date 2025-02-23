from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from bot.handling.states.main_menu import MainMenuSG

router = Router()


@router.message(Command("start"))
async def handler(msg: Message, dialog_manager: DialogManager):
    await dialog_manager.start(state=MainMenuSG.menu, mode=StartMode.RESET_STACK)
