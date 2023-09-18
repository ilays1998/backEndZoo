from __future__ import annotations
import strawberry
import typing
from typing import List

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


url = strawberry.scalar(
    typing.NewType("url", str),
    parse_value=lambda v: str(v)
)

@strawberry.type
class Animal(Node):
    name: str
    image: url
    age: int
    @strawberry.field
    def metadata(self) -> AnimalMetadata:
        if self.name == "snake":
            return AnimalMetadata(domain="Eukaryota",
                                  kingdom="Animalia",
                                  pyhlum="Chordata",
                                  _class="Reptilia",
                                  superfamily="Squamata",
                                  family="Serpentes")
    @strawberry.

    @classmethod
    def from_dict(cls, data: dict) -> Animal:
        return Animal(**data)



DB = {
    "animals": {
        [
            Animal(
                name="snake",
                image="https://sensorytools.net/cdn/shop/products/1_98351ebe-0205-4a5c-b121-f987fa950fce.png?v=1681262929",
                age=5
            ),
            Animal(
                name="lion",
                image="https://th-thumbnailer.cdn-si-edu.com/7-edQjVy53tlGD2OhGdl-mrY1K8=/fit-in/1600x0/https%3A%2F%2Ftf-cmsv2-smithsonianmag-media.s3.amazonaws.com%2Ffiler%2Fa9%2Fff%2Fa9ff31d0-aecd-464e-80c7-873e4651cd2b%2Fmufasa.jpeg",
                age=23
            )
        ]
    },
    "metadata": {
        [
            AnimalMetadata(domain="Eukaryota",
                           kingdom="Animalia",
                           pyhlum="Chordata",
                           _class="Reptilia",
                           superfamily="Squamata",
                           family="Serpentes"),
            AnimalMetadata(domain="Eukaryota",
                           kingdom="Animalia",
                           pyhlum="Chordata",
                           _class="Mammalia",
                           superfamily="Felidae",
                           family="Pantherinae")
        ]
    }
}

#
# type Animal implements Node {
#     name: String!
#     image: URL!
#     age: Int!
#     metadata: AnimalMetadata!
# }







def get_animals() -> List[Animal]:
    return []


@strawberry.type
class Query:
    animals: List[Animal] = strawberry.field(resolver=get_animals)

schema = strawberry.Schema(query=Query, types=[Node, Animal])



