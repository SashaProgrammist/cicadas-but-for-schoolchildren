
class Book:
    books = dict()

    currents_page = dict()


    def __init__(self, name, count_page):
        self.name = name

        self.count_page = count_page

        Book.books[self.name] = self

    def get_page(self, index):
        return {
            0: "This is the text of page 5 of Book1.",
            1: "This is the text of page 12 of Book1."
        }[index]
