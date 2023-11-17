from server.canvas.constants import ShapeType


class CanvasElement:
    shape_type: ShapeType
    x: int
    y: int
    attributes: dict


class CanvasStore:
    elements: list[CanvasElement]

    def top_layer(self):
        return len(self.elements)

    def add(self, element: CanvasElement):
        self.elements.append(element)

    def remove(self, element: CanvasElement):
        self.elements.remove(element)

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
