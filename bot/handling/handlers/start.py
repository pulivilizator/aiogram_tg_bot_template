from aiogram import Router
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.filters import Command
from aiogram.types import Message, TelegramObject
from aiogram_dialog import DialogManager
from dishka.integrations.aiogram import FromDishka
from sqlalchemy.ext.asyncio import AsyncSession

router = Router()

@router.message(Command("start"))
async def handler(msg: Message, dialog_manager: DialogManager, r: FromDishka[AiohttpSession]):
    print(r)
    await msg.answer('hello')