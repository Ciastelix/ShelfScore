from db import Base
from models.user import User
from models.book import Book
from models.review import Review
from models.author import Author

# Add all your models to the Base metadata
target_metadata = Base.metadata
