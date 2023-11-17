from __future__ import annotations

import abc
from server.canvas.canvas_store import CanvasElement, CanvasStore
from server.canvas.constants import ShapeType, ActionTypeCodes, DELIMITER_CHAR


class BaseAction(abc.ABC):
    @abc.abstractmethod
    def do(self, canvas: CanvasStore):
        ...

    @abc.abstractmethod
    def reverse_action(self) -> BaseAction:
        ...


class AddShape(BaseAction):
    shape: CanvasElement
    idx: int = -1

    def __init__(self, shape_type: ShapeType, x: int, y: int, **kwargs: dict) -> None:
        self.shape_type = shape_type
        self.x = x
        self.y = y
        self.kwargs = kwargs
        self.shape = CanvasElement(shape_type=shape_type, x=x, y=y, attributes=kwargs)

    def do(self, canvas: CanvasStore):
        self.element_uid = canvas.add(self.shape, self.idx)

    def reverse_action(self):
        return RemoveShape(self.element_uid)

    def encode(self):
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
        self.shape = canvas.get_element_by_id(self.element_uid)
        self.idx = canvas.get_element_layer(self.shape)
        canvas.remove(self.shape)

    def reverse_action(self):
        return AddShape(
            self.shape.shape_type,
            self.shape.x,
            self.shape.y,
            **self.shape.attributes,
        )

    def encode(self):
        return DELIMITER_CHAR.join(
            map(
                str,
                (
                    ActionTypeCodes.remove_shape,
                    self.element_uid,
                ),
            )
        )
