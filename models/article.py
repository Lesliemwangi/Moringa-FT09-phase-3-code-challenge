import sqlite3
from database.connection import get_db_connection
from models.author import Author
from models.magazine import Magazine


class Article:
    def __init__(self, id, title, content, author_id, magazine_id):
        self.id = id
        self.title = title
        self.content = content
        self.author_id = author_id
        self.magazine_id = magazine_id

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not isinstance(value, str):
            raise ValueError("Article title must be a string")
        if not (5 <= len(value) <= 50):
            raise ValueError(
                "Article title must be between 5 and 50 characters")
        self._title = value

    @staticmethod
    def create(author, magazine, title):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)",
                       (title, "", author.id, magazine.id))
        conn.commit()
        article_id = cursor.lastrowid
        conn.close()
        return Article(article_id, title, "", author.id, magazine.id)

    def author(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT authors.* FROM authors INNER JOIN articles ON authors.id = articles.author_id WHERE articles.id=?", (self.id,))
        author_data = cursor.fetchone()
        conn.close()
        return Author(author_data['id'], author_data['name'])

    def magazine(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT magazines.* FROM magazines INNER JOIN articles ON magazines.id = articles.magazine_id WHERE articles.id=?", (self.id,))
        magazine_data = cursor.fetchone()
        conn.close()
        return Magazine(magazine_data['id'], magazine_data['name'], magazine_data['category'])

    def __repr__(self):
        return f'<Article {self.title}>'
