from server.conference.constants import (
    ActionTypeCodes,
    DELIMITER_CHAR,
    ActionStatusCode,
)
from server.conference.actions.actions import *


ActionTypeCodeTable: dict[ActionTypeCodes, BaseAction] = {
    ActionTypeCodes.add_shape: AddShape,
    ActionTypeCodes.remove_shape: RemoveShape
    # TODO: continue
}


class ActionEncoding:
    @staticmethod
    def decode(signal: str) -> tuple[BaseAction, int]:
        signal_id, action_type_code, *args = map(int, signal.split(DELIMITER_CHAR))
        action = ActionTypeCodeTable[action_type_code](*args)
        return action, signal_id

    @staticmethod
    def encode_action(action: BaseAction):
        fields = action.get_fields()
        return DELIMITER_CHAR.join(
            map(
                str,
                fields.values(),
            )
        )

    @staticmethod
    def encode_action_response(
        signal_id: int, status_code: ActionStatusCode, response_body: list[int]
    ):
        return DELIMITER_CHAR.join(
            map(
                str,
                [
                    signal_id,
                    status_code,
                ]
                + response_body,
            )
        )
