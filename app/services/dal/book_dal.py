from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.books import Book
from app.services.dal.dto.book_dto import BookDTO


class BookDal:
    @staticmethod
    def create_book(db: Session, title: str, department: str, file_path: str, created_by: int) -> Book:
        new_book = Book(
            title=title,
            department=department,
            file_path=file_path,
            created_by=created_by
        )
        db.add(new_book)
        db.commit()
        db.refresh(new_book)
        return new_book

    @staticmethod
    def get_book_by_id(db: Session, book_id: int) -> Optional[BookDTO]:
        book = db.query(Book).filter(Book.id == book_id, Book.is_active).first()
        return BookDTO.to_dto(book) if book else None

    @staticmethod
    def get_books_by_department(db: Session, department: str) -> List[BookDTO]:
        books = db.query(Book).filter(Book.department == department, Book.is_active).all()
        return [BookDTO.to_dto(book) for book in books]

    @staticmethod
    def update_book(db: Session, book_id: int, **kwargs) -> Optional[Book]:
        book = db.query(Book).filter(Book.id == book_id, Book.is_active).first()
        if not book:
            return None

        for key, value in kwargs.items():
            if hasattr(book, key):
                setattr(book, key, value)
        db.commit()
        db.refresh(book)
        return book

    @staticmethod
    def delete_book(db: Session, book_id: int) -> bool:
        book = db.query(Book).filter(Book.id == book_id, Book.is_active).first()
        if not book:
            return False
        book.is_active = False
        db.commit()
        return True