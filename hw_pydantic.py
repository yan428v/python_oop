from pydantic import BaseModel, EmailStr
from typing import List, Optional


class Book(BaseModel):
    title: str
    author: str
    year: int
    available: bool = True
    categories: List[str]

class User(BaseModel):
    name: str
    email: EmailStr
    membership_id: str

class Library(BaseModel):
    books: List[Book] = []
    users: List[User] = []

    def total_books(self) -> int:
        return len(self.books)


def add_book(books: List[Book], book: Book)-> None:
    books.append(book)


class BookNotAvailable(Exception):
    pass


def find_book(books: List[Book], title: str) -> Optional[Book]:
        for b in books:
            if b.title == title:
                return b

        return None


def is_book_borrow(books: List[Book], title: str) -> Book:

    for b in books:
        if b.title == title and b.available == True:
            b.available = False
            return b
        else: raise BookNotAvailable(f"книга уже взята")

    raise BookNotAvailable(f'книга не найдена')


def return_book(books: List[Book], title: str) -> Optional[Book]:

    for b in books:
        if b.title == title and b.available == False:
            b.available = True
            return b

    return None

def log_operation(func):
    def wrapper(*args, **kwargs):
        print(f"вызов: {func.__name__}")
        result = func(*args, **kwargs)
        print(f"завершено: {func.__name__}")
        return result
    return wrapper