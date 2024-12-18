from fastapi import FastAPI
from container import Container
import uvicorn
from routes import user, book, review, author
from main_routes import router

container = Container()
db = container.db()
db.create_database()
app = FastAPI()
app.container = container
app.include_router(user.router, prefix="/users")
app.include_router(book.router, prefix="/books")
app.include_router(review.router, prefix="/reviews")
app.include_router(author.router, prefix="/authors")
app.include_router(router)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)
