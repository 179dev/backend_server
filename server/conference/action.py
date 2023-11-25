from __future__ import annotations


class Action:
    target_canvas_id: int
    canvas_data: str

    @classmethod
    def cook_data(cls, raw_data: dict) -> Action:
        return Action(
            target_canvas_id=int(raw_data["target"]), canvas_data=raw_data["drawing"]
        )

    def __init__(self, target_canvas_id: int, canvas_data: str) -> None:
        self.target_canvas_id = target_canvas_id
        self.canvas_data = canvas_data

    def to_json(self) -> dict:
        return {
            "type": "broadcast",
            "target": self.target_canvas_id,
            "drawing": self.canvas_data,
        }
