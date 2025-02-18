from cmath import rect
from typing import Any
from pygame import Rect
from Handlers.Flags import SubscriptionType


class Subscription():
    def __init__(self, type: SubscriptionType, callback: Any):
        self.type = type
        self.callback = callback


class InputSubscribtion(Subscription):
    def __init__(self, type: SubscriptionType, callback: Any, cursor: Rect, keys):
        super().__init__(type, callback)
        self.condition_cursor = cursor
        # Debug RECT!
        self.condition_keys = keys

    def get_type(self) -> SubscriptionType:
        return self.type

    def check_condition(self, cursor: tuple[int, int], keys: list[int], mouse_buttons: tuple[bool, bool, bool]) -> None:
        match self.type:
            case SubscriptionType.ALL:
                print(f"[Subscription] ALL:\tCURSOR: {cursor}\tKEYS: {keys}")
                in_rect = self.point_in_rect(cursor)
                keys_pressed = self.condition_keys in keys
                if in_rect and keys_pressed:
                    self.callback(cursor, keys)
            case SubscriptionType.CURSOR:
                print(f"[Subscription] CURSOR: {cursor}")
                if self.point_in_rect(cursor):
                    self.callback(cursor)
            case SubscriptionType.KEYS:
                print(f"[Subscription] KEYS: {keys}")
                if self.condition_keys in keys:
                    self.callback(keys)
            case _:
                pass

    def point_in_rect(self, cursor: tuple[int, int]) -> bool:
        x1 = self.condition_cursor.x
        y1 = self.condition_cursor.y
        width = self.condition_cursor.width
        height = self.condition_cursor.height
        x2 = x1 + width
        y2 = y1 + height

        point_x = cursor[0]
        point_y = cursor[1]

        if x1 <= point_x and point_x <= x2:
            if y1 <= point_y and point_y <= y2:
                return True
        return False
