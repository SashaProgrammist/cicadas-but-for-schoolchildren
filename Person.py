import sqlite3
from aiogram.types import Message
from abc import ABC, abstractmethod


class DoubleCreatePersons(Exception):
    pass


class DoubleCreatePlayer(Exception):
    pass


class InterfacePersons(ABC):
    @abstractmethod
    def add_person(self, massage: Message):
        pass

    @abstractmethod
    def get_question(self, table: str, id_que: int) -> tuple[str, str] | None:
        pass

    @abstractmethod
    def update_person(self, set_db: str, params: tuple) -> None:
        pass


class Persons(InterfacePersons):
    self: None | InterfacePersons = None

    def __init__(self):
        self.conn = sqlite3.connect('data/test.db')
        self.cursor = self.conn.cursor()

        self.conn.commit()

        if Persons.self is None:
            Persons.self = self
        else:
            raise DoubleCreatePersons()

    def add_person(self, massage: Message):
        username = massage.from_user.username
        chat_id = massage.chat.id

        self.cursor.execute('SELECT chat_id FROM players WHERE chat_id = ?', (chat_id, ))
        is_have = len(self.cursor.fetchall())

        if not is_have:
            self.cursor.execute('INSERT INTO players (username, chat_id, role) VALUES (?, ?, ?)',
                                (username, chat_id, "player"))

            self.conn.commit()
        else:
            raise DoubleCreatePlayer()

    def get_question(self, table: str, id_que: int) -> tuple[str, str] | None:
        self.cursor.execute(f'SELECT que, ans FROM {table} WHERE id = ?', (id_que, ))
        data = self.cursor.fetchall()
        if data:
            return data[0]
        else:
            return None

    def update_person(self, set_db: str, params: tuple) -> None:
        self.cursor.execute(f'UPDATE players SET {set_db} WHERE chat_id=?', params)
        self.conn.commit()


if __name__ == "__main__":
    print("do init")
    if int(input()):
        # Создание подключения к базе данных
        _conn = sqlite3.connect('data/test.db')
        _cursor = _conn.cursor()

        _cursor.execute('DELETE FROM players WHERE id = ?', (2,))
        _conn.commit()
