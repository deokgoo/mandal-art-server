from typing import List
from pymongo import MongoClient
import strawberry
import typing
from fastapi import FastAPI
from strawberry.asgi import GraphQL

client = MongoClient("mongodb://root:example@mongo:27017/")
db = client.library

@strawberry.type
class Book:
  title: str
  author: str

@strawberry.type
class Author:
  name: str
  books: typing.List[Book]

@strawberry.type
class Query:
    hello: str = strawberry.field(resolver=lambda: "Hello World!")
    books: List[Book] = strawberry.field(resolver= lambda: [Book(
        title=book['title'],
        author=book['author']
    ) for book in db.books.find()])
    authors: List[Author] = strawberry.field(resolver= lambda: [Author(
        name=author['name'],
        books=[Book(title=book['title'], author=book['author']) for book in db.books.find({"author": author.name})]
    ) for author in db.authors.find()])

@strawberry.input
class AddBookInput:
  title: str = strawberry.field(description="The title of the book")
  author: str = strawberry.field(description="The name of the author")

@strawberry.type
class Mutation:
  @strawberry.mutation
  def add_book(self, book:AddBookInput) -> Book:
    db.books.insert_one({'title': book.title, 'author':book.author })
    print(f'Adding {book.title} by {book.title}')
    return Book(title=book.title, author=book.author)


# mutation {
#   addBook(book: {
#     title: "hia",
#     author: "hellbo"
#   }) {
#     title
#     author
#   }
# }


schema = strawberry.Schema(query=Query, mutation=Mutation)

graphql_app = GraphQL(schema)

app = FastAPI()
app.add_route("/q", graphql_app)
app.add_websocket_route("/q", graphql_app)
