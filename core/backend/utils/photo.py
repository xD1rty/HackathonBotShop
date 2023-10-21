import aiohttp
from io import BytesIO
from aiogram.types import Message
from core.config import get_config


# async def download_photos(photos: list):
#     result = []
#     path = BytesIO()
#     await photo[-1].download(destination_file=path)
#     return photo[-1].file


async def upload_photos(photos: list):
    result = []
    for photo in photos:
        path = BytesIO()
        await photo.download(destination_file=path)
        async with aiohttp.ClientSession() as session:
            async with session.post(
                    f'http://freeimage.host/api/1/upload/?key={get_config(".env").API_KEY}&source={photo.file}&format=json'
            ) as response:
                result.append((await response.json())['image']['url'])
    return result
