import aiohttp
from io import BytesIO
from aiogram.types import Message
from core.config import get_config


async def download_photo(photo: Message.photo):
    path = BytesIO()
    await photo[-1].download(destination_file=path)
    return photo[-1].file


async def upload_photo(photo):

    async with aiohttp.ClientSession() as session:
        async with session.post(
                f'http://freeimage.host/api/1/upload/?key={get_config(".env").API_KEY}&source={photo}&format=json'
        ) as response:
            return await response.json()
