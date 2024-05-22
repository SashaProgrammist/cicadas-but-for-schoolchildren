import os
import pdf2image
from pdf2image import convert_from_path
from PIL.Image import Image
from os import listdir
from os.path import isfile, join

POPPLER_PATH = r'C:\Program Files\Release-24.02.0-0\poppler-24.02.0\Library\bin'


class Book:
    books = dict()

    currents_page = dict()

    def __init__(self, name, count_page, name_file):
        self.name = name
        self.count_page = count_page
        self.name_file = name_file

        Book.books[self.name] = self

    def get_page(self, index, id_user) -> str:
        name = f"img_{self.name_file}_{index}_"

        result = [f for f in listdir("hash/") if name in f]
        while not result:
            _ = convert_from_path(f"D:/my_doc/programm/cicadas-but-for-schoolchildren/books/{self.name_file}.pdf",
                                  first_page=index, last_page=index,
                                  poppler_path=POPPLER_PATH,
                                  output_folder=r"D:\my_doc\programm\cicadas-but-for-schoolchildren\hash",
                                  fmt="png", output_file=name)

            result = [f for f in listdir("hash/") if name in f]

        result = "hash/" + result[0]

        Book.currents_page[id_user] = result

        return result
