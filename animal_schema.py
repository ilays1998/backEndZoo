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
    #id: strawberry.ID
    name: str
    image: url
    age: int
    metadata: AnimalMetadata

    @classmethod
    def from_dict(cls, data_animal: dict, data_metadata: dict) -> Animal:
        meta = AnimalMetadata(id=data_metadata['id'],
                              domain=data_metadata['domain'],
                              kingdom=data_metadata['kingdom'],
                              pyhlum=data_metadata['pyhlum'],
                              _class=data_metadata['_class'],
                              superfamily=data_metadata['superfamily'],
                              family=data_metadata['family'])
        animal = Animal(id=data_animal['id'],
                        name=data_animal['name'],
                        image=data_animal['image'],
                        age=data_animal['age'],
                        metadata=meta)
        return animal


# DB = {
#     "animals": {
#         [
#             Animal(
#                 id="1",
#                 name="snake",
#                 image="https://sensorytools.net/cdn/shop/products/1_98351ebe-0205-4a5c-b121-f987fa950fce.png?v=1681262929",
#                 age=5
#             ),
#             Animal(
#                 id='2',
#                 name="lion",
#                 image="https://th-thumbnailer.cdn-si-edu.com/7-edQjVy53tlGD2OhGdl-mrY1K8=/fit-in/1600x0/https%3A%2F%2Ftf-cmsv2-smithsonianmag-media.s3.amazonaws.com%2Ffiler%2Fa9%2Fff%2Fa9ff31d0-aecd-464e-80c7-873e4651cd2b%2Fmufasa.jpeg",
#                 age=23
#             )
#         ]
#     },
#     "metadata": {
#         [AnimalMetadata(domain="Eukaryota",
#                         kingdom="Animalia",
#                         pyhlum="Chordata",
#                         _class="Reptilia",
#                         superfamily="Squamata",
#                         family="Serpentes"),
#          AnimalMetadata(domain="Eukaryota",
#                         kingdom="Animalia",
#                         pyhlum="Chordata",
#                         _class="Mammalia",
#                         superfamily="Felidae",
#                         family="Pantherinae")]
#     }
#
# }

DB = {
    "animals": [
        {
            "id": "1",
            "name": "snake",
            "image": "https://sensorytools.net/cdn/shop/products/1_98351ebe-0205-4a5c-b121-f987fa950fce.png?v=1681262929",
            "age": 5,
        },
        {
            "id": "2",
            "name": "lion",
            "image": "https://th-thumbnailer.cdn-si-edu.com/7-edQjVy53tlGD2OhGdl-mrY1K8=/fit-in/1600x0/https%3A%2F%2Ftf-cmsv2-smithsonianmag-media.s3.amazonaws.com%2Ffiler%2Fa9%2Fff%2Fa9ff31d0-aecd-464e-80c7-873e4651cd2b%2Fmufasa.jpeg",
            "age": 23,
        },
    ],
    "metadata": [
        {
            "id": "2",
            "domain": "Eukaryota",
            "kingdom": "Animalia",
            "pyhlum": "Chordata",
            "_class": "Mammalia",
            "superfamily": "Felidae",
            "family": "Pantherinae",
        },
        {
            "id": "1",
            "domain": "Eukaryota",
            "kingdom": "Animalia",
            "pyhlum": "Chordata",
            "_class": "Reptilia",
            "superfamily": "Squamata",
            "family": "Serpentes",
        }
    ],
}




#
# type Animal implements Node {
#     name: String!
#     image: URL!
#     age: Int!
#     metadata: AnimalMetadata!
# }


def get_animals() -> List[Animal]:
    result = []
    for animal in DB['animals']:
        animal_id = animal['id']
        for meta in DB['metadata']:
            if animal_id == meta['id']:
                result.append(Animal.from_dict(animal, meta))
                break
    return result

@strawberry.type
class Query:
    animals: List[Animal] = strawberry.field(resolver=get_animals)


schema = strawberry.Schema(query=Query, types=[Node, Animal])
