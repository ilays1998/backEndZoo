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


def get_animals() -> list[Animal]:
    animals = models.Animal.objects.all()
    return [Animal.from_orm(obj) for obj in animals]


@strawberry.type
class Query:
    animals: list[Animal] = strawberry.field(resolver=get_animals)


schema = strawberry.Schema(query=Query, types=[Node, Animal])
(Path(__file__).parent / "schema.graphql").write_text(str(schema))