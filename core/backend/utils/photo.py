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


async def upload_photo(photo_size: PhotoSize, bot: Bot):
    photo_path = (await bot.get_file(photo_size.file_id)).file_path
    destination = BytesIO()
    async with aiohttp.ClientSession() as session:
        data = aiohttp.FormData()
        data.add_field('image',
                       await bot.download_file(photo_path, destination=destination),
                       content_type='multipart/form-data')
        async with session.post(
                f'https://api.imgbb.com/1/upload?expiration=600&key={get_config(".env").API_KEY}', data=data
        ) as response:
            return (await response.json())['data']['url']
