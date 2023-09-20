from __future__ import annotations

import typing
# merge to main
from pathlib import Path

import strawberry
from typing import Optional
from strawberry.field_extensions import InputMutationExtension

from backend.animals import models
from django.core.exceptions import ObjectDoesNotExist


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
    # id: strawberry.ID
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


def get_metadata() -> list[AnimalMetadata]:
    metadata = models.Metadata.objects.all()
    return [AnimalMetadata.from_orm(obj) for obj in metadata]


def get_nodes() -> list[Node]:
    result = get_animals()
    result += get_metadata()
    return result


@strawberry.type
class Query:
    animals: list[Animal] = strawberry.field(resolver=get_animals)
    nodes: list[Node] = strawberry.field(resolver=get_nodes)


@strawberry.input
class MetadataInput:
    domain: str
    kingdom: str
    pyhlum: str
    _class: str
    superfamily: str
    family: str


@strawberry.input
class AnimalInput:
    name: str
    image: url
    age: int
    metadata_id: Optional[strawberry.ID] = None
    metadata_family_name: Optional[str] = None



@strawberry.type
class Mutation:
    @strawberry.field
    def add_metadata(self, input: MetadataInput) -> \
            AnimalMetadata:
        new_metadat = models.Metadata.objects.create(
            domain=input.domain,
            kingdom=input.kingdom,
            pyhlum=input.pyhlum,
            _class=input._class,
            superfamily=input.superfamily,
            family=input.family)

        new_metadat.save()

        return AnimalMetadata.from_orm(new_metadat)

    @strawberry.mutation
    def add_animal(self, input: AnimalInput) -> Animal:
        # Create a new Animal instance with the provided input data
        if input.metadata_id is None and input.metadata_family_name is None:
            raise ObjectDoesNotExist("you have to give either an id or family_name")
        if input.metadata_id is not None:
            metadata = models.Metadata.objects.get(pk=input.metadata_id)
        else:
            metadata = models.Metadata.objects.get(family=input.metadata_family_name)
        new_animal = models.Animal.objects.create(
            name=input.name,
            image=input.image,
            age=input.age,
            metadata=metadata
        )

        new_animal.save()

        return Animal.from_orm(new_animal)


schema = strawberry.Schema(query=Query, mutation=Mutation)
(Path(__file__).parent / "schema.graphql").write_text(str(schema))
