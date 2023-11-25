from __future__ import annotations

import abc
from server.conference.canvas_store import CanvasElement, CanvasStore
from server.conference.constants import ShapeType, ActionTypeCodes, DELIMITER_CHAR


class BaseAction(abc.ABC):
    canvas_id: int

    @abc.abstractmethod
    def do(self, canvas: CanvasStore):
        ...

    @abc.abstractmethod
    def reverse_action(self) -> BaseAction:
        ...

    @abc.abstractmethod
    def encode(self) -> str:
        ...


class AddShape(BaseAction):
    shape: CanvasElement
    idx: int = -1

    def __init__(
        self, canvas_id: int, shape_type: ShapeType, x: int, y: int, **kwargs: dict
    ) -> None:
        self.canvas_id = canvas_id
        self.shape_type = shape_type
        self.x = x
        self.y = y
        self.kwargs = kwargs
        self.shape = CanvasElement(shape_type=shape_type, x=x, y=y, attributes=kwargs)

    def do(self, canvas: CanvasStore):
        self.element_uid = canvas.add(self.shape, self.idx)

    def reverse_action(self):
        return RemoveShape(self.canvas_id, self.element_uid)

    def encode(self) -> str:
        return DELIMITER_CHAR.join(
            map(
                str,
                (
                    ActionTypeCodes.add_shape,
                    self.canvas_id,
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

    def __init__(self, canvas_id: int, element_uid: int) -> None:
        self.canvas_id = canvas_id
        self.element_uid = element_uid

    def do(self, canvas: CanvasStore):
        self.shape = canvas.get_element_by_id(self.element_uid)
        self.idx = canvas.get_element_layer(self.shape)
        canvas.remove(self.shape)

    def reverse_action(self):
        return AddShape(
            self.canvas_id,
            self.shape.shape_type,
            self.shape.x,
            self.shape.y,
            **self.shape.attributes,
        )

    def encode(self) -> str:
        return DELIMITER_CHAR.join(
            map(
                str,
                (
                    ActionTypeCodes.remove_shape,
                    self.canvas_id,
                    self.element_uid,
                ),
            )
        )
