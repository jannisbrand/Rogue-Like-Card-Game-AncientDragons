

import pygame
from Handlers.Event_Handler import Event_Handler
from Handlers.Flags import SubscriptionType
from Handlers.Subscriptions.Types import InputSubscribtion, Subscription


class InputHandler(Event_Handler):
    def __init__(self, application):
        super().__init__(application)
        self.pressed_keys_in_frame = []
        self.current_cursor_position = ()
        self.pressed_mouse_buttons_in_frame = ()
        self.subscriptions = []

        # ### TEST ### #
        self.wait_time = 0
        self.standard_click_delay = 1

    def subscribe_to_event(self, subscription: Subscription) -> None:
        self.subscriptions.append(subscription)

    def update(self, events: list[pygame.event.Event]) -> None:
        """Updates the handler and updates the cursor position
        (Events only handle moving cursors :))
        """
        if self.wait_time > 0:
            self.wait_time -= 1
            return
        self.wait_time = 0

        self.handle_input_events(events)

        # ### CONTINIOUS ### #
        self.current_cursor_position = pygame.mouse.get_pos()
        self.handle_mouse_position()

    def handle_input_events(self, events: list[pygame.event.Event]) -> None:
        """Events specificly for presses, releases, etc...
        """
        for event in events:
            match event.type:
                case pygame.KEYDOWN:
                    self.pressed_keys_in_frame.append(event.key)
                case pygame.MOUSEMOTION:
                    cursor_position = pygame.mouse.get_pos()
                    self.current_cursor_position = cursor_position
                case pygame.MOUSEBUTTONDOWN:  # DRAG
                    self.pressed_mouse_buttons_in_frame = pygame.mouse.get_pressed()
                case pygame.MOUSEBUTTONUP:
                    self.pressed_mouse_buttons_in_frame = pygame.mouse.get_pressed()

        self.handle_key_down()

        self.pressed_keys_in_frame = []


    def handle_key_down(self) -> None:
        for subscription in self.subscriptions:
            if not subscription.is_active():
                break
            if subscription.get_type() == SubscriptionType.KEYS:
                subscription.check_condition(self.current_cursor_position, self.pressed_keys_in_frame, self.pressed_mouse_buttons_in_frame)
            if subscription.get_type() == SubscriptionType.MOUSEBUTTON:
                subscription.check_condition(self.current_cursor_position, self.pressed_keys_in_frame, self.pressed_mouse_buttons_in_frame)

    def handle_mouse_movement(self) -> None:
        for subscription in self.subscriptions:
            if not subscription.is_active():
                break
            if subscription.get_type() == SubscriptionType.CURSOR:
                subscription.check_condition(self.current_cursor_position, self.pressed_keys_in_frame, self.pressed_mouse_buttons_in_frame)

    def handle_mouse_position(self) -> None:
        for subscription in self.subscriptions:
            if not subscription.is_active():
                break
            subscription_type = subscription.get_type()
            match subscription_type:
                case SubscriptionType.CURSOR:
                    subscription.check_condition(self.current_cursor_position, self.pressed_keys_in_frame, self.pressed_mouse_buttons_in_frame)

    def reset(self) -> None:
        self.pressed_keys_in_frame = []
        self.current_cursor_position = ()
        self.pressed_mouse_buttons_in_frame = ()
        self.subscriptions = []

    def set_wait(self, time) -> None:
        self.wait_time = (time * 60)  # * delta_time

    def remove_subscribtion(self, subscribtion: InputSubscribtion):
        try:
            self.subscriptions.remove(subscribtion)
        except ValueError as e:
            print("[INPUTHANDLER] Subscribtion does not exist:", e)
