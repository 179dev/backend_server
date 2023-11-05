import drawsvg
from drawsvg import Drawing


class ActionType:
    add_shape = 1
    remove_shape = 2
    add_handle = 3
    remove_handle = 4
    edit_shape_param = 5


class ShapeType:
    rectangle = 1
    ellipsis = 2
    circle = 3
    line = 4


DELIMITER_CHAR = ";"


class Action:
    values: list[int]
    raw_signal: str

    def __init__(self, signal: str):
        self.values = list(map(int, signal.split(DELIMITER_CHAR)))

    def perform(self, drawing: Drawing):
        action_type, *args = self.values
        match action_type:
            case ActionType.add_shape:
                shape_id, x, y, *shape_args = args
                match shape_id:
                    case ShapeType.rectangle:
                        w, h = shape_args
                        shape = drawsvg.Rectangle(x, y, w, h)
                drawing.append(shape)


DELIMITER_BYTE = 127


class ActionByte:
    values: list[int]
    raw_signal: bytes

    def __init__(self, signal: bytes):
        self.raw_signal = signal
        seq = []
        split_bytes = []
        for b in signal:
            if b == DELIMITER_BYTE:
                split_bytes.append(int.from_bytes(bytes(seq)))
                seq = []
            else:
                seq.append(b)
        split_bytes.append(int.from_bytes(bytes(seq)))
        self.values = split_bytes

    def perform(self, drawing: Drawing):
        action_type, *args = self.values
        match action_type:
            case ActionType.add_shape:
                shape_id, x, y, *shape_args = args
                match shape_id:
                    case ShapeType.rectangle:
                        w, h = shape_args
                        shape = drawsvg.Rectangle(x, y, w, h)
                drawing.append(shape)
