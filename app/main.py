import numbers
from turtle import tilt
from typing import List
from pymongo import MongoClient
import strawberry
import typing
from fastapi import FastAPI
from strawberry.asgi import GraphQL

client = MongoClient("mongodb://root:example@mongo:27017/")
db = client.mandala

@strawberry.type
class Mandal:
  title: str
  childs: typing.List[str]


@strawberry.type
class Query:
    @strawberry.field
    def mandals(self) -> List[Mandal]:
      return [Mandal(
        title=mandal['title'],
        childs=mandal['childs']
      ) for mandal in db.mandals.find()]

    @strawberry.field
    def mandal(self, title: str) ->Mandal:
      m = db.mandals.find_one({'title': title})
      return Mandal(title=m['title'], childs=m['childs'])

@strawberry.type
class Mutation:
  @strawberry.mutation
  def set_mandal(self, title: str, childs: typing.List[str]) -> None:

    if db.mandals.find_one({'title': title}) is None:
      db.mandals.insert_one({
        'title': title, 
        'childs': childs 
      })
    else:
      db.mandals.find_one_and_replace({'title': title}, {
        'title': title, 
        'childs': childs 
      })
  @strawberry.mutation
  def delete_mandal(self, title: str) -> None:
    db.mandals.delete_one({'title': title})

schema = strawberry.Schema(query=Query, mutation=Mutation)

graphql_app = GraphQL(schema)

app = FastAPI()
app.add_route("/q", graphql_app)
app.add_websocket_route("/q", graphql_app)
