import asyncio
import logging
import sys
from os import getenv
from typing import Any, Dict
import sqlite3

from aiogram import Bot, Dispatcher, F, Router, html
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

from Person import Persons

form_router = Router()


class AxesState(StatesGroup):
    continue_state = State()


@form_router.message(AxesState.continue_state)
async def process_name(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    is_first = data["is_first"]
    question_id = data["question_id"]

    if is_first:
        que = Persons.self.get_question("moder_que", question_id)
        await state.update_data(is_first=False, que=que)
        await message.answer(que[0])
    else:
        que = data["que"]

        if message.text == que[1]:
            que = Persons.self.get_question("moder_que", question_id + 1)

            await message.answer("OK")

            if que is None:
                Persons.self.update_person("role=?", ("moder", message.chat.id))

                await message.answer("update role")
                await state.clear()
            else:
                await state.update_data(que=que, question_id=question_id + 1)

                await message.answer(que[0])
        else:
            await message.answer("No")


@form_router.message(Command('giv_me_moder'))
async def command_start(message: Message, state: FSMContext) -> None:
    await state.set_state(AxesState.continue_state)

    await state.update_data(question_id=1, is_first=True)

    await message.answer(
        "выход - /cancel",
        reply_markup=ReplyKeyboardRemove(),
    )

    await process_name(message, state)


async def show_summary(message: Message, data: Dict[str, Any], positive: bool = True) -> None:
    name = data["name"]
    language = data.get("language", "<something unexpected>")
    text = f"I'll keep in mind that, {html.quote(name)}, "
    text += (
        f"you like to write bots with {html.quote(language)}."
        if positive
        else "you don't like to write bots, so sad..."
    )
    await message.answer(text=text, reply_markup=ReplyKeyboardRemove())


def init_begin_moder(dp):
    dp.include_router(form_router)


if __name__ == "__main__":
    pass
