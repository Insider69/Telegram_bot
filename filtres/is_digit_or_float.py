from aiogram.types import Message
from aiogram.filters import BaseFilter, CommandObject
from typing import Any


class CheckForDigit(BaseFilter):
    
    async def __call__(self, message: Message, **data: Any):
        # print(data)
        command: CommandObject = data.get('command')
        try:
            arg = command.args
            
            if arg.isnumeric() or (arg.count('.') == 1 and arg.replace('.', '').isnumeric()):
                return True
            return False
        except Exception:
            await message.reply('⚠️ Warning --> Введите количество')