from __future__ import annotations

import abc
from server.canvas.canvas_store import CanvasElement, CanvasStore
from server.canvas.constants import ShapeType, ActionTypeCodes, DELIMITER_CHAR


class BaseAction(abc.ABC):
    @abc.abstractmethod
    def do(self, canvas: CanvasStore):
        """
        A method that needs to be implemented by subclasses. It represents
        the main functionality of the class.

        Parameters:
            canvas (CanvasStore): An object representing the canvas store.

        Returns:
            None
        """
        ...

    @abc.abstractmethod
    def reverse_action(self) -> BaseAction:
        """
        Reverse the action and return the resulting BaseAction.

        Returns:
            BaseAction: The reversed action.
        """
        ...

    @abc.abstractmethod
    def encode(self) -> str:
        """
        A method that encodes the data and returns it as a string.

        Returns:
            str: The encoded data as a string.
        """
        ...


class AddShape(BaseAction):
    shape: CanvasElement
    idx: int = -1

    def __init__(self, shape_type: ShapeType, x: int, y: int, **kwargs: dict) -> None:
        """
        Initializes a new instance of the class.

        Args:
            shape_type (ShapeType): The type of shape.
            x (int): The x-coordinate of the shape.
            y (int): The y-coordinate of the shape.
            **kwargs (dict): Additional keyword arguments.

        Returns:
            None
        """
        self.shape_type = shape_type
        self.x = x
        self.y = y
        self.kwargs = kwargs
        self.shape = CanvasElement(shape_type=shape_type, x=x, y=y, attributes=kwargs)

    def do(self, canvas: CanvasStore):
        """
        Adds the shape to the canvas and sets the element's local ID.

        Args:
            canvas (CanvasStore): The canvas on which the action will be performed.

        Returns:
            None
        """
        self.element_uid = canvas.add(self.shape, self.idx)

    def reverse_action(self):
        """
        Reverses the action of the current element (removes it).
        Is used for undo/redo.

        Return:
            An instance of the RemoveShape class with the element UID as the parameter.
        """
        return RemoveShape(self.element_uid)

    def encode(self) -> str:
        """
        Encodes the object which must be added into a string representation.

        Returns:
            str: The encoded string.
        """
        return DELIMITER_CHAR.join(
            map(
                str,
                (
                    ActionTypeCodes.add_shape,
                    self.shape_type,
                    self.x,
                    self.y,
                    self.element_uid,
                    # Extend on the attrs here
                ),
            )
        )


class RemoveShape(BaseAction):
    element_uid: int

    def __init__(self, element_uid: int) -> None:
        self.element_uid = element_uid

    def do(self, canvas: CanvasStore):
        """
        Remove the shape from the canvas.

        Args:
            canvas (CanvasStore): The canvas store object.

        Returns:
            None
        """
        self.shape = canvas.get_element_by_id(self.element_uid)
        self.idx = canvas.get_element_layer(self.shape)
        canvas.remove(self.shape)

    def reverse_action(self):
        """
        Reverses the action performed by the current shape (adds it).
        Is used for undo/redo.

        Returns:
            AddShape: A new instance of the AddShape class with the same shape type, x and y coordinates, and attributes as the original shape.
        """
        return AddShape(
            self.shape.shape_type,
            self.shape.x,
            self.shape.y,
            **self.shape.attributes,
        )

    def encode(self) -> str:
        """
        Encodes the object which must be added into a string representation.

        Returns:
            str: The encoded string.
        """
        return DELIMITER_CHAR.join(
            map(
                str,
                (
                    ActionTypeCodes.remove_shape,
                    self.element_uid,
                ),
            )
        )
