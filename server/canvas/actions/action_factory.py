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
        """
        Decode the given signal and return the corresponding BaseAction object.

        Parameters:
            signal (str): The signal to decode.

        Returns:
            BaseAction: The decoded BaseAction object.

        Raises:
            ValueError: If the signal is not properly formatted.

        Example:
            decode("1;2;3") -> ActionTypeCodeTable[1](2, 3)
        """
        action_type_code, *args = map(int, signal.split(DELIMITER_CHAR))
        return ActionTypeCodeTable[action_type_code](*args)
