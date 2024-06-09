from database.connection import get_db_connection
from models.author import Author
from models.magazine import Magazine


class Article:
    def __init__(self, id, title, content, author_id, magazine_id):
        # Initialize an Article object with id, title, content, author_id, and magazine_id
        self.id = id
        self.title = title
        self.content = content
        self.author_id = author_id
        self.magazine_id = magazine_id

    @property
    def title(self):
        # Getter for the title property, returning the title of the article
        return self._title

    @title.setter
    def title(self, value):
        # Setter for the title property, ensuring it's a string between 5 and 50 characters
        if not isinstance(value, str):
            raise ValueError("Article title must be a string")
        if not (5 <= len(value) <= 50):
            raise ValueError(
                "Article title must be between 5 and 50 characters")
        self._title = value

    @staticmethod
    def create(author, magazine, title):
        # Create a new Article object and save it to the database
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Execute an INSERT query to add a new article to the database
        cursor.execute("INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)",
                       (title, "", author.id, magazine.id))
        conn.commit()
        article_id = cursor.lastrowid
        conn.close()
        # Return a new Article object with the generated ID and provided title, content, author_id, and magazine_id
        return Article(article_id, title, "", author.id, magazine.id)

    def author(self):
        # Retrieve the author associated with this article from the database
        conn = get_db_connection()
        cursor = conn.cursor()
        # Execute a SELECT query to retrieve the author data from the database
        cursor.execute(
            "SELECT authors.* FROM authors INNER JOIN articles ON authors.id = articles.author_id WHERE articles.id=?", (self.id,))
        
        author_data = cursor.fetchone()
        conn.close()
        # Return an Author object with the retrieved data
        return Author(author_data['id'], author_data['name'])

    def magazine(self):
        # Retrieve the magazine associated with this article from the database
        conn = get_db_connection()
        cursor = conn.cursor()
        # Execute a SELECT query to retrieve the magazine data from the database
        cursor.execute(
            "SELECT magazines.* FROM magazines INNER JOIN articles ON magazines.id = articles.magazine_id WHERE articles.id=?", (self.id,))
        magazine_data = cursor.fetchone()
        conn.close()
        # Return a Magazine object with the retrieved data
        return Magazine(magazine_data['id'], magazine_data['name'], magazine_data['category'])

    def __repr__(self):
        # Return a string representation of the Article object.
        return f'<Article {self.title}>'
