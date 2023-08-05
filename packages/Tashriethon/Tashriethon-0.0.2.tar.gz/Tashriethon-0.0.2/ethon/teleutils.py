"""This file is part of the ethon distribution.
Copyright (c) 2021 vasusen-code
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, version 3.
This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
General Public License for more details.
License can be found in < https://github.com/Tashri2342/ethon/blob/main/LICENSE > ."""

#Tashri-Code/thechariotoflight/TashriBots
#__TG:TashriBots__
from telethon import events

#to mention
async def mention(bot, id):
    a = await bot.get_entity(int(id))
    x = a.first_name
    return f'[{x}](tg://user?id={id})'
