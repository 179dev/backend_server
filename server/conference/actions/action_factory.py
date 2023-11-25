from server.conference.constants import ActionTypeCodes, DELIMITER_CHAR
from server.conference.actions.actions import *


ActionTypeCodeTable: dict[ActionTypeCodes, BaseAction] = {
    ActionTypeCodes.add_shape: AddShape,
    ActionTypeCodes.remove_shape: RemoveShape
    # TODO: continue
}


class ActionDecoder:
    @staticmethod
    def decode(signal: str) -> BaseAction:
        action_type_code, *args = map(int, signal.split(DELIMITER_CHAR))
        action = ActionTypeCodeTable[action_type_code](*args)
        return action
