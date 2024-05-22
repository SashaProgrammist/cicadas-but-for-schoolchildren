import asyncio
import logging
import sys
from os import getenv, remove
import cv2
import numpy as np

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile, BufferedInputFile
from aiogram.filters.command import Command

from Book import Book, Image
from Templates import Template

f = open("API_TOKEN.txt", "r")
try:
    API_TOKEN = f.read()
finally:
    f.close()

TOKEN = getenv(API_TOKEN)

dp = Dispatcher()


@dp.message(Command('start'))
async def send_welcome(message: Message):
    await message.reply("Welcome to the game! Use /get <book> <page> "
                        "to get a page and /impose <template> to apply a template.")


@dp.message(Command('get'))
async def get_page(message: Message):
    try:
        _, book, page = message.text.split()
        page = int(page)
        image: None | str = None
        try:
            image = Book.books[book].get_page(page)
        except Exception as e:
            logging.error(e)
            print("images file")

        if image:
            print(image)
            image_file = FSInputFile(image)
            await message.reply_photo(image_file, caption=f'Page {page}')
        else:
            await message.reply("Page not found.")
    except Exception as e:
        logging.error(e)
        await message.reply("Usage: /get <book> <page>")


@dp.message(Command('impose'))
async def impose_template(message: Message):
    try:
        template_id = " ".join(message.text.split()[1:])
        if message.from_user.id in Book.currents_page:
            text = Book.currents_page[message.from_user.id]
            if template_id in Template.templates:
                modified_text = Template.templates[template_id].temp(text)
                await message.reply(f"Modified text: {modified_text}")
            else:
                await message.reply("Template not found.")
        else:
            await message.reply("No page loaded. Use /get first.")
    except Exception as e:
        await message.reply("Usage: /impose <template>")


async def main() -> None:

    bot = Bot(token=API_TOKEN)

    await dp.start_polling(bot)


def init():
    Book("Book1", 2, "B1")

    Template("== 0",
             (lambda text: ''.join([char for idx, char in enumerate(text) if idx % 2 == 0])))
    Template("!= 0",
             (lambda text: ''.join([char for idx, char in enumerate(text) if idx % 2 != 0])))


if __name__ == '__main__':
    init()
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
