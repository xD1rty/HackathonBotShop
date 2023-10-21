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
    print(photo_path)
    destination = BytesIO()
    async with aiohttp.ClientSession() as session:
        data = aiohttp.FormData()
        data.add_field('file',
                       open('Front.jpg', 'rb'),
                       filename='Front.jpg',
                       content_type='multipart/form-data')
        async with session.post(
                f'http://freeimage.host/api/1/upload/?key={get_config(".env").API_KEY}&format=json',
                data=data
        ) as response:
            print(await response.json(), response)
            return (await response.json())['image']['url']
