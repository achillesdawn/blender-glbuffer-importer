import bpy
import json
from typing import TypedDict

IMPORT_PATH = "/home/miguel/python/glbuffer_importer/data.json"


class Indices(TypedDict):
    _elements: dict[str, int]


class Primitive(TypedDict):
    mode: str
    count: int
    offset: int
    indices: Indices
    uType: int


class GeoExporter(TypedDict):
    name: str
    vertices: dict[str, int]
    primitives: list[Primitive]


class SimpleShapeData(TypedDict):
    vertices: dict[int, float]
    primitives: dict[int, float]


class ShapeData(TypedDict):
    _vertices: dict[int, float]
    _primitiveIndices: dict[int, int]
    _vertexIndices: dict[int, int]


def load_data():
    with open(IMPORT_PATH, "r") as f:
        data: list[GeoExporter] = json.load(f)

    print("data are loaded")
    return data


def get_triangles_mode_strip(
    primitives: list[Primitive],
) -> list[tuple[int, int, int]]:  # -> list[Any]:
    for primitive in primitives:

        print(primitive.keys())

        print("mode", primitive["mode"])
        print("offset", primitive["offset"])

        if primitive["mode"] != 5:
            continue

        indices = list(primitive["indices"]["_elements"].values())

        print("indices len:", len(indices))

        triangles: list[tuple[int, int, int]] = []
        for i in range(len(indices) - 2):
            # For even-numbered triangles, keep vertex order
            # For odd-numbered triangles, swap second and third vertices
            if i % 2 == 0:
                triangle = (indices[i], indices[i + 1], indices[i + 2])
            else:
                triangle = (indices[i], indices[i + 2], indices[i + 1])
                
            if triangle[0] != triangle[1] and triangle[1] != triangle[2] and triangle[0] != triangle[2]:
                triangles.append(triangle)

        return triangles
    return []


def create_object(shape_data: list[GeoExporter]):
    assert bpy.context

    for model in shape_data:
        mesh = bpy.data.meshes.new(model["name"])
        vertices = model["vertices"]
        vertices = list(vertices.values())
        vertices = [vertices[i : i + 3] for i in range(0, len(vertices), 3)]

        faces = get_triangles_mode_strip(model["primitives"])

        mesh.from_pydata(vertices=vertices, edges=[], faces=faces)
        ob = bpy.data.objects.new("buffer_object", mesh)
        bpy.context.scene.collection.objects.link(ob)


shape_data = load_data()
create_object(shape_data)


# create_object(shape_data)
