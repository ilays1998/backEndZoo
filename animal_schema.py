from __future__ import annotations
import strawberry
import typing
from typing import List
AnimalMetadata(

)
DB = {
    "animals": {
        [
            Animal()
        ]
    },
    "metadata"
}
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
#
# type Animal implements Node {
#     name: String!
#     image: URL!
#     age: Int!
#     metadata: AnimalMetadata!
# }






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

    @classmethod
    def from_dict(cls, data: dict) -> Animal:
        return Animal(**data)

def get_animals() -> List[Animal]:
    return [Animal(
        name="snake",
        image="https://sensorytools.net/cdn/shop/products/1_98351ebe-0205-4a5c-b121-f987fa950fce.png?v=1681262929",
        age=5
    ),
        Animal(
            name="snake",
            image="https://sensorytools.net/cdn/shop/products/1_98351ebe-0205-4a5c-b121-f987fa950fce.png?v=1681262929",
            age=23
        )]


@strawberry.type
class Query:
    animals: List[Animal] = strawberry.field(resolver=get_animals)


schema = strawberry.Schema(query=Query)



