from database.connection import get_db_connection

class Author:
    def __init__(self, id, name):
        # Initialize an Author object with id and name
        self.id = id
        # Set the name of the author
        self.name = name

    @property
    def id(self):
        # Getter for the id property
        return self._id

    @id.setter
    def id(self, value):
        # Setter for the id property, ensuring it's an integer
        if not isinstance(value, int):
            raise ValueError("Author ID must be of type int")
        self._id = value

    @property
    def name(self):
        # Getter for the name property
        return self._name

    @name.setter
    def name(self, value):
        # Setter for the name property, ensuring it's a non-empty string
        if not isinstance(value, str):
            raise ValueError("Author name must be a string")
        if len(value) == 0:
            raise ValueError("Author name must not be empty")
        self._name = value

    @staticmethod
    def create(name):
        # Create a new Author object and insert it into the database
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Insert the author's name into the database
        cursor.execute("INSERT INTO authors (name) VALUES (?)", (name,))
        
        # Commit the changes and retrieve the inserted author's ID
        conn.commit()
        
        # Get the ID of the newly created author
        author_id = cursor.lastrowid
        
        # Close the database connection
        conn.close()
        
        # Return a new Author object with the inserted author's ID and name
        return Author(author_id, name)

    def articles(self):
        # Retrieve all articles associated with this author from the database
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Retrieve all articles associated with this author from the 
        # Query the database for articles with the current author's ID
        cursor.execute("SELECT * FROM articles WHERE author_id=?", (self.id,))
        
        articles = cursor.fetchall()
        conn.close()
        return articles

    def magazines(self):
        # Retrieve all magazines associated with this author from the database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT DISTINCT magazines.* FROM magazines INNER JOIN articles ON magazines.id = articles.magazine_id WHERE articles.author_id=?", (self.id,))
        magazines = cursor.fetchall()
        conn.close()
        return magazines

    def __repr__(self):
        # Return a string representation of the Author object.
        return f'<Author {self.name}>'
