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
        """
        Initializes a new instance of the class.

        Parameters:
            None

        Returns:
            None
        """
        self.elements = []
        self.registered_elements = set()
        self.local_ids_table = {}

    def top_layer(self):
        return len(self.elements)

    def register_if_isnt_already(self, element: CanvasElement):
        """
        Registers an element if it is not already registered and returns its local ID.

        Args:
            element (CanvasElement): The element to be registered.

        Returns:
            int: The local ID of the registered element.
        """
        if element in self.registered_elements:
            return element._local_id
        self.registered_elements.add(element)
        self.local_ids_table[self.id_counter] = element
        uid = element._local_id = self.id_counter
        self.id_counter += 1
        return uid

    def add(self, element: CanvasElement, idx: SupportsIndex = -1):
        """
        Adds an element to the canvas.

        Args:
            element (CanvasElement): The element to be added to the canvas.
            idx (SupportsIndex, optional): The index at which the element should be inserted. Defaults to -1.

        Returns:
            int: The local ID of the registered element.
        """
        if idx == -1:
            self.elements.append(element)
        else:
            self.elements.insert(idx, element)
        return self.register_if_isnt_already(element)

    def remove(self, element: CanvasElement):
        """
        Remove the specified element from the list of canvas elements.

        Parameters:
            element (CanvasElement): The element to be removed.

        Returns:
            None
        """
        self.elements.remove(element)

    def get_element_by_id(self, id: int):
        """
        Retrieves the element from the local IDs table based on the provided ID.

        Parameters:
            id (int): The ID of the element to retrieve.

        Returns:
            The element associated with the provided ID.
        """
        return self.local_ids_table[id]

    def get_element_layer(self, element: CanvasElement):
        """
        Returns the layer of a given CanvasElement within the list of elements.

        Parameters:
            element (CanvasElement): The CanvasElement whose layer is to be retrieved.

        Returns:
            int: The number of the layer of the CanvasElement within the list of elements.
        """
        return self.elements.index(element)

    def move_element_up(self, element: CanvasElement):
        """
        Moves the specified canvas element up in the list of elements in it's layer.

        Parameters:
            element (CanvasElement): The canvas element to move up.

        Returns:
            None
        """
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
        """
        Move an element down in the list of layer elements.

        Args:
            element (CanvasElement): The element to move down.

        Returns:
            None
        """
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
        """
        Move the given element to the top of the elements list in a layer.
        
        Parameters:
            element (CanvasElement): The element to be moved.
        
        Returns:
            None
        """
        if element not in self.elements:
            return
        self.elements.remove(element)
        self.elements.append(element)

    def move_element_bottom(self, element: CanvasElement):
        """
        Moves the given element to the bottom of the list of elements in a layer.

        Args:
            element (CanvasElement): The element to be moved.

        Returns:
            None
        """
        if element not in self.elements:
            return
        self.elements.remove(element)
        self.elements.insert(0, element)
