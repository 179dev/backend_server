from server.canvas.constants import ActionTypeCodes, DELIMITER_CHAR
from server.canvas.actions.actions import *


ActionTypeCodeTable = {
    ActionTypeCodes.add_shape: AddShape,
    ActionTypeCodes.remove_shape: RemoveShape
    # TODO: continue
}


class ActionDecoder:
    @staticmethod
    def decode(signal: str) -> BaseAction:
        action_type_code, *args = signal.split(DELIMITER_CHAR)
        return ActionTypeCodeTable[action_type_code](*args)
