from typing import Any
from pygame import Rect
import pygame
from Handlers.Flags import SubscriptionType


class Subscription():
    def __init__(self, type: SubscriptionType, source: Any, callback: Any):
        self.active = True
        self.type = type
        self.source = source
        self.callback = callback

    def get_type(self) -> SubscriptionType:
        return self.type

    def is_active(self) -> bool:
        return self.active

    def deactivate(self) -> None:
        self.active = False

    def activate(self) -> None:
        self.active = True


class InputSubscribtion(Subscription):
    def __init__(self, type: SubscriptionType, source: Any, callback: Any, cursor: Rect = None, keys: list[int] = [], mouse_buttons: tuple[bool, bool, bool] = ()):
        super().__init__(type, source, callback)
        self.condition_cursor = cursor
        # Debug RECT!
        self.condition_keys = keys
        self.condition_mouse_buttons = mouse_buttons

        self.last_pressed = 0

    def check_condition(self, cursor: tuple[int, int], keys: list[int], mouse_buttons: tuple[bool, bool, bool]) -> None:
        """
        TODO: Implementation of the mouse buttons"""
        match self.type:
            case SubscriptionType.ALL:
                in_rect = self.point_in_rect(cursor)
                keys_pressed = self.check_key(keys)
                if in_rect and keys_pressed:
                    print(f"[Subscription] ALL:\tCURSOR: {cursor}\tKEYS: {keys}")
                    self.callback(self.source, cursor, keys)
            case SubscriptionType.CURSOR:
                if self.point_in_rect(cursor):
                    print(f"[Subscription] CURSOR: {cursor}")
                    self.callback(self.source, cursor)
            case SubscriptionType.KEYS:
                if self.check_key(keys):
                    print(f"[Subscription] KEYS: {keys}")
                    self.callback(self.source, keys)
            case SubscriptionType.MOUSEBUTTON:
                in_rect = self.point_in_rect(cursor)
                keys_pressed = self.check_mouse_button(mouse_buttons)
                if in_rect and keys_pressed:
                    print(f"[Subscription] MOUSEBUTTON: {mouse_buttons}")
                    self.callback(self.source, mouse_buttons)
                    self.last_pressed = pygame.time.Clock().get_rawtime()
            case _:
                pass

    def point_in_rect(self, cursor: tuple[int, int]) -> bool:
        try:
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
        except IndexError as e:
            print(f"[Subscription] Cursor not in window area: {e}")
            return False

    def check_key(self, keys: list[int]) -> bool:
        check = len(keys) > 0
        for key in keys:
            if key in self.condition_keys:
                pass
            else:
                check = False
        return check

    def check_mouse_button(self, mouse_buttons: tuple[bool]) -> bool:
        index = 0
        check = len(mouse_buttons) > 0
        try:
            for mouse_button in mouse_buttons:
                if mouse_button != self.condition_mouse_buttons[index]:
                    check = False
                index += 1
            return check
        except IndexError as e:
            print(f"[Subscription] No mouse buttons to check! {e}", self.source.get_name())
        return False
