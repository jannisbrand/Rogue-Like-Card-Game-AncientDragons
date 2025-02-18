from typing import Any
import pygame

from Handlers.Flags import SubscriptionType


class Event_Handler():
    def __init__(self, application):
        self.__application_context = application
        self.player_controller: None

        self.subscriptions: list

    def handle_events(self):
        for event in pygame.event.get():
            match event.type:
                case pygame.KEYDOWN:
                    self.__key_down_events(event)
                case pygame.KEYUP:
                    self.__key_up_events(event)

    def __key_down_events(self, event: pygame.event):
        print("[EVENTHANDLER]KEYDOWN]" + str(event.key))

    def __key_up_events(self, event: pygame.event):
        print("[EVENTHANDLER]KEYUP]" + str(event.key))
