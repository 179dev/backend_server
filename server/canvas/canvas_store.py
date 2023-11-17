from server.canvas.constants import ShapeType
from typing import SupportsIndex


class CanvasElement:
    shape_type: ShapeType
    x: int
    y: int
    attributes: dict
    _local_id: int

    def __init__(self, shape_type: ShapeType, x: int, y: int, attributes: dict):
        self.shape_type = shape_type
        self.x = x
        self.y = y
        self.attributes = attributes


class CanvasStore:
    # TODO: pythonic list probably isn't the most efficient
    # data structure for this task, better replace it with
    # something more optimized after the MVP
    elements: list[CanvasElement]

    # TODO: mutex'ify these for good
    registered_elements: set[CanvasElement]
    local_ids_table: dict[int, CanvasElement]
    id_counter: int = 0

    def __init__(self) -> None:
        self.elements = []
        self.registered_elements = set()
        self.local_ids_table = {}

    def top_layer(self):
        return len(self.elements)

    def register_if_isnt_already(self, element: CanvasElement):
        if element in self.registered_elements:
            return element._local_id
        self.registered_elements.add(element)
        self.local_ids_table[self.id_counter] = element
        uid = element._local_id = self.id_counter
        self.id_counter += 1
        return uid

    def add(self, element: CanvasElement, idx: SupportsIndex = -1):
        if idx == -1:
            self.elements.append(element)
        else:
            self.elements.insert(idx, element)
        return self.register_if_isnt_already(element)

    def remove(self, element: CanvasElement):
        self.elements.remove(element)

    def get_element_by_id(self, id: int):
        return self.local_ids_table[id]

    def get_element_layer(self, element: CanvasElement):
        return self.elements.index(element)

    def move_element_up(self, element: CanvasElement):
        if element not in self.elements:
            return
        idx = self.elements.index(element)
        if idx + 1 == len(self.elements):
            return
        self.elements[idx], self.elements[idx + 1] = (
            self.elements[idx + 1],
            self.elements[idx],
        )

    def move_element_down(self, element: CanvasElement):
        if element not in self.elements:
            return
        idx = self.elements.index(element)
        if idx == 0:
            return
        self.elements[idx - 1], self.elements[idx] = (
            self.elements[idx],
            self.elements[idx - 1],
        )

    def move_element_top(self, element: CanvasElement):
        if element not in self.elements:
            return
        self.elements.remove(element)
        self.elements.append(element)

    def move_element_bottom(self, element: CanvasElement):
        if element not in self.elements:
            return
        self.elements.remove(element)
        self.elements.insert(0, element)
