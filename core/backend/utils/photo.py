import aiohttp
from io import BytesIO
from aiogram.types import Message
from core.config import get_config
from aiogram.client.bot import Bot
from aiogram.types import PhotoSize


# async def download_photos(photos: list):
#     result = []
#     path = BytesIO()
#     await photo[-1].download(destination_file=path)
#     return photo[-1].file


async def upload_photo(photo: PhotoSize, bot: Bot):
    photo_path = (await bot.get_file(photo.file_id)).file_path
    destination = BytesIO()
    async with aiohttp.ClientSession() as session:
        async with session.post(
                f'http://freeimage.host/api/1/upload/?key={get_config(".env").API_KEY}&source={await bot.download_file(photo_path, destination=destination)}&format=json'
        ) as response:
            return (await response.json())['image']['url']
