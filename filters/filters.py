from aiogram.enums import ChatType
from aiogram.filters import BaseFilter
from aiogram.types import Message
from aiogram.filters import Filter
from aiogram import Bot
from config import chenel_id


class GroupFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]
    

class ChenelSub(Filter):
    async def __call__(self, message:Message, bot:Bot):
        user_status = await bot.get_chat_member(chenel_id[0], message.from_user.id)
        if user_status in ["creator", "administrator", "member"]:
            user_status2 = await bot.get_chat_member(chenel_id[1], message.from_user.id)
            if user_status2 in ["creator", "administrator", "member"]:
                return True
            return False
        return False