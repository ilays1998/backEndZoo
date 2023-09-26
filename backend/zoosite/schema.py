from __future__ import annotations

import time
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
    #time.sleep(5)
    animals = models.Animal.objects.all()
    return [Animal.from_orm(obj) for obj in animals]


def get_metadata() -> list[AnimalMetadata]:
    metadata = models.Metadata.objects.all()
    return [AnimalMetadata.from_orm(obj) for obj in metadata]


@strawberry.type
class Query:
    animals: list[Animal] = strawberry.field(resolver=get_animals)


@strawberry.input
class MetadataInput:
    domain: str
    kingdom: str
    pyhlum: str
    _class: str
    superfamily: str
    family: str


@strawberry.type()
class AddMetaDataPayload:
    data: AnimalMetadata | None = None
    error: str | None = None


@strawberry.type()
class RemoveMetaDataPayload:
    data: str | None = None
    error: str | None = None


@strawberry.input
class AnimalInput:
    name: str
    image: url
    age: int
    metadata_id: Optional[strawberry.ID] = None
    metadata_family_name: Optional[str] = None


@strawberry.type()
class AddAnimalPayload:
    data: Animal | None = None
    error: str | None = None


@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_metadata(self, input: MetadataInput) -> \
            AddAnimalPayload:
        new_metadat = models.Metadata.objects.create(
            domain=input.domain,
            kingdom=input.kingdom,
            pyhlum=input.pyhlum,
            _class=input._class,
            superfamily=input.superfamily,
            family=input.family)

        new_metadat.save()

        return AddAnimalPayload(data=AnimalMetadata.from_orm(new_metadat))

    @strawberry.mutation
    def remove_metadata_by_id(self, pk: int) -> RemoveMetaDataPayload:
        try:
            meta = models.Metadata.objects.get(pk=pk)
        except:
            return RemoveMetaDataPayload(error="There isn't a Metadata object with this pk in the database")

        data = meta.__str__()
        meta.delete()
        return RemoveMetaDataPayload(data=("delete: " + data))

    @strawberry.mutation
    def remove_Animal_by_name(self, name: str) -> RemoveMetaDataPayload:
        try:
            meta = models.Animal.objects.get(name=name)
        except:
            return RemoveMetaDataPayload(error="There isn't a Metadata object with this name in the database")

        data = meta.__str__()
        meta.delete()
        return RemoveMetaDataPayload(data=("delete: " + data))

    @strawberry.mutation
    def add_animal(self, input: AnimalInput) -> AddAnimalPayload:
        # Create a new Animal instance with the provided input data
        if input.metadata_id is None and input.metadata_family_name is None:
            AddAnimalPayload(error="you have to give either an id or family_name")
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

        return AddAnimalPayload(data=Animal.from_orm(new_animal))


schema = strawberry.Schema(query=Query, mutation=Mutation)
(Path(__file__).parent / "schema.graphql").write_text(str(schema))
