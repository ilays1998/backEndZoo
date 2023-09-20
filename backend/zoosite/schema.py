from __future__ import annotations

from pathlib import Path

import strawberry
import typing

from backend.animals import models


@strawberry.interface
class Node:
    id: strawberry.ID


@strawberry.type
class AnimalMetadata(Node):
    domain: str
    kingdom: str
    pyhlum: str
    _class: str
    superfamily: str
    family: str
    @staticmethod
    def from_orm(orm: models.Metadata) -> AnimalMetadata:
        return AnimalMetadata(
            id=orm.pk,
            domain=orm.domain,
            kingdom=orm.kingdom,
            pyhlum=orm.pyhlum,
            _class=orm._class,
            superfamily=orm.superfamily,
            family=orm.family
        )

url = strawberry.scalar(
    typing.NewType("url", str),
    parse_value=lambda v: str(v)
)


@strawberry.type
class Animal(Node):
    #id: strawberry.ID
    name: str
    image: url
    age: int
    metadata: AnimalMetadata

    @staticmethod
    def from_orm(orm: models.Animal) -> Animal:
        meta = AnimalMetadata.from_orm(orm.metadata)
        animal = Animal(id=orm.pk,
                        name=orm.name,
                        image=orm.image,
                        age=orm.age,
                        metadata=meta)
        return animal


# DB = {
#     "animals": [
#         {
#             "id": "1",
#             "name": "snake",
#             "image": "https://sensorytools.net/cdn/shop/products/1_98351ebe-0205-4a5c-b121-f987fa950fce.png?v=1681262929",
#             "age": 5,
#         },
#         {
#             "id": "2",
#             "name": "lion",
#             "image": "https://th-thumbnailer.cdn-si-edu.com/7-edQjVy53tlGD2OhGdl-mrY1K8=/fit-in/1600x0/https%3A%2F%2Ftf-cmsv2-smithsonianmag-media.s3.amazonaws.com%2Ffiler%2Fa9%2Fff%2Fa9ff31d0-aecd-464e-80c7-873e4651cd2b%2Fmufasa.jpeg",
#             "age": 23,
#         },
#     ],
#     "metadata": [
#         {
#             "id": "2",
#             "domain": "Eukaryota",
#             "kingdom": "Animalia",
#             "pyhlum": "Chordata",
#             "_class": "Mammalia",
#             "superfamily": "Felidae",
#             "family": "Pantherinae",
#         },
#         {
#             "id": "1",
#             "domain": "Eukaryota",
#             "kingdom": "Animalia",
#             "pyhlum": "Chordata",
#             "_class": "Reptilia",
#             "superfamily": "Squamata",
#             "family": "Serpentes",
#         }
#     ],
# }


#
# type Animal implements Node {
#     name: String!
#     image: URL!
#     age: Int!
#     metadata: AnimalMetadata!
# }


def get_animals() -> list[Animal]:
    animals = models.Animal.objects.all()
    return [Animal.from_orm(obj) for obj in animals]


@strawberry.type
class Query:
    animals: list[Animal] = strawberry.field(resolver=get_animals)


schema = strawberry.Schema(query=Query, types=[Node, Animal])
(Path(__file__).parent / "schema.graphql").write_text(str(schema))