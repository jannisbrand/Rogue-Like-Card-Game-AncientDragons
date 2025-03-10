from typing import Type, Any, cast

import pygame

from Characters import Base
from Characters.Boss_Enemy import BossEnemy
from Characters.Player_Character import PlayerCharacter
from Characters.Standard_Enemy import StandardEnemy
from Sprites.Base import Sprite
from Components import Components, Effects

"""
TODO:
    - Für die Typen der Komponenten entscheiden.
        -> Was sind sie? (Klasse; Struct; ...; ...)
        -> Wie sind sie strukturiert?

    - Für den "Speicher-Ort" der Komponenten entscheiden.
        -> Die SQL-Datenbank? (Macht aber eigentlich keinen Sinn! Instanzen und so..)
        -> Eigene Text-/Python-File?
        -> Oder was ganz anderes?

    - Die Komponenten definieren.
        -> Die Karteneigenschaften zu ECS-Komponenten übersetzen

-------------------------------------------------------------------------
    Grobe Beschreibung..
    
    Prozessbeginn:
    - Der Initiale Applikationstand wird hergestellt.
        -> Applikations Kontext wird erstellt.
        -> Event handler werden erstellt.
        -> ECS Kontext wird erstellt.
        -> Render Kontext wird erstellt.
        -> Entity Factory wird erstellt.

    - Die Entity Factory, bekommt/ließt die Karten-Daten aus der Datenbank.
        -> Entities werden erstellt
        -> Komponenten werden erstellt und den Entieties zugewiesen.

    - Der ECS Kontext, wird von der Entity Factory mit Karten gefüllt.
        -> Die erstellten Entities, sowie die alle erstellten Komponenten, die den Entities zugewiesen sind, sind hier.

    - Die Charakter Factory, bekommt/ließt die Daten aus der Datenbank.
        -> Die Charakter Klassen werden erstellt.
        -> Die Entity Id's, die den Standart-Karten der Charaktere entsprechen, werden den Klassen übergeben.

    Future:
    - Der Game Mode wird erstellt. (Wie genau ist die Frage.. Datenbank, oder einfach Hard-Code)
    - Die Level Factory bekommt/ließt die Daten aus der Datenbank.
        -> Mit einem statischen seed, wird mit dem Abschluss eines Levels ein weiteres generiert.
"""


class ECSO_Context():
    def __init__(self):
        # ### ENTITIES AND COMPONENTS # ###
        self.entities: set[int] = set() # Collection of all id's
        # Mapping specific components mapped to entities to component types
        self.components: dict[Type, dict[int, Any]] = {}
        self.next_entity_id = 1
        self.number_of_registered_entities: int = 0
        # ### ENTITIES AND COMPONENTS # ###

        # ### OBJECTS ### #
        self.game_objects: dict[Type, dict[int, Any]] = {}
        # self.next_object_id = 1  # TODO: DOES NOT REPRESENT THE RIGHT AMOUNT OF OBJECTS PER TYPE!
        # ### OBJECTS ### #

    def add_entity(self) -> int:
        """Creates a new entity in the context

        Returns:
            int: Id of the newly created entity
        """
        new_entity_id = self.next_entity_id
        self.entities.add(new_entity_id)
        self.next_entity_id += 1
        self.number_of_registered_entities += 1
        return new_entity_id

    def add_component(self, entity: int, component: Any) -> None:
        """Mapps an instance of a component to an entity.

        Args:
            entity (int): The id of the entity
            component (instance): An instance of an component class
        """
        component_type = type(component)

        if component_type not in self.components:
            # Creates a new dictionary for a missing component type
            self.components[component_type] = {}    # This!

        self.components[component_type][entity] = component

    def add_components(self, entity: int, components: list[Any]) -> None:
        """Mapps an instance of a component to an entity.

        Args:
            entity (int): The id of the entity
            component (instance): An instance of an component class
        """
        for component in components:
            component_type = type(component)

            if component_type not in self.components:
                # Creates a new dictionary for a missing component type
                self.components[component_type] = {}    # This!

            self.components[component_type][entity] = component

    def get_components(self, entity: int) -> list[Any]:
        """Returns a list of components

        Args:
            entity (int): The id of the entity

        Returns:
            list[any]: A list of component classes. 
            Returns [] if there are none.
        """
        components_of_entity = []
        for component_type in self.components:
            try:
                component = self.components[component_type][entity]
                components_of_entity.append(component)
                print(component)
            except KeyError as e:
                # Example: If an entity has only one component but there are 10 component types registered the exception will be risen 9 times. :)  
                print(f"[ECSOContext] Entity {e} does not has component: {component_type}!")
                continue
            
        return components_of_entity

    def get_component(self, entity: int, component_type: Any) -> Any:
        try:
            return self.components[component_type][entity]
        except KeyError as e:
            print(f"[ECSOContext] Entity {e} does not has component: {component_type}!")
            return None

    def get_entity(self, component_type: Any, value: str) -> int:
        for entity in self.entities:
            try:
                if self.components[component_type][entity].value == value:
                    return entity
            except KeyError as e:
                print(f"[ECSOContext] Entity {e} does not have component: {component_type}")
        return -1

    def add_game_object(self, entity: int, game_object: Any) -> int:
        try:
            instance_type = type(game_object)
            if instance_type not in self.game_objects:
                self.game_objects[instance_type] = {}

            self.game_objects[instance_type][entity] = game_object
        except KeyError as e:
            print(f"[ECSOContext] Object could not be added: {e}")
            return -1

    def add_game_objects(self, entity: int, game_objects: list[Any]) -> None:
        try:
            for game_object in game_objects:
                self.add_game_object(entity, game_object)  # Smart :)
        except KeyError as e:
            print(f"[ECSOContext] Objects could not be added: {e}")

    def get_game_objects(self, entity: int) -> list[Any]:
        list_of_game_objects = []
        for game_object_type in self.game_objects:
            try:
                if entity in self.game_objects[game_object_type]:
                    game_object = self.game_objects[game_object_type][entity]
                    list_of_game_objects.append(game_object)
            except KeyError as e:
                print(f"[ECSOContext] Entity {e} does not has game_object of type: {game_object}!")
                continue

        return list_of_game_objects
    
    def get_game_objects_of_type(self, game_object_type: Any) -> set[int, Any]:
        try:
            return self.game_objects[game_object_type].items()
        except AttributeError as e:
            print("[ECSOContext] Attribute not initialised:", e)
            return ()

    def get_game_object(self, entity: int, game_object_type: Any = None) -> Any:
        try:
            if entity in self.game_objects[game_object_type]:
                return self.game_objects[game_object_type][entity]
            else:
                return None
        except AttributeError as e:
            print("[ECSOContext] Attribute not initialised:", e)
            return None
        except KeyError:
            return None
        except Exception as e:
            print(e)

    def is_game_object_enity_existent(self, entity: int) -> bool:
        for game_object_type, game_objects in self.game_objects.items():
            if entity in self.game_objects[game_object_type]:
                return True
        return False
 
    def get_game_object_types(self) -> list[Any]:
        try:
            list_of_game_object_types = []
            for game_object_types, _ in self.game_objects.items():
                list_of_game_object_types.append(game_object_types)

            return list_of_game_object_types
        except AttributeError as e:
            print("[ECSOContext] Attribute not initialised:", e)
            return None
        
    def get_game_object_entities(self) -> list[int]:
        try:
            game_object_entities = []
            for game_object_type, _ in self.game_objects.items():
                for entity in self.entities:
                    if entity in self.game_objects[game_object_type]:
                        game_object_entities.append(entity)
            return game_object_entities
        except AttributeError as e:
            print("[ECSOContext] An attribute is not initialised:", e)
            return []


    def remove_game_object(self, entity: int) -> None:
        try:
            for game_object_type, game_objects in self.game_objects.items():
                try: 
                    game_object = game_objects.pop(entity)
                    del game_object
                    self.entities.discard(entity)  # TEST
                except KeyError:
                    continue
        except KeyError as e:
            print("", e)

    def attack_modifiers(self, value_to_modify, list_of_components) -> int:
        for comp in list_of_components:
            match comp:
                case Components.C_ATTACK_PLUS:
                    value_to_modify + comp.value
                    pass
                case Components.C_ATTACK_ALL:
                    # We only have one enemy currently
                    pass
                case Components.C_ATTACK_RANDOM:
                    # still only one enemy. It will target the one enemy
                    pass
                case Components.C_ATTACK_NUM:
                    # the value of the component is the number of seperate attacks
                    pass
                case Components.C_ATTACK_INCREASE:
                    value_to_modify + comp.value
                    # attack is increased by the cards played
                    # need to check the played cards
                    pass
                case Components.C_ATTACK_MULT:
                    value_to_modify * comp.value
                    pass
                case Components.C_EXHAUST_ATK:
                    # for every exhausted card gain extra atk
                    # need to get the number of exhausted cards before
                    value_to_modify + comp.value 
                    pass
        return value_to_modify
            
    def card_system(self, selected_card: int,selected_type: Any, selected_target: int) -> bool:
        components = self.get_components(selected_card)
        target = self.get_game_object(selected_target, selected_type)
        
        for component in components:
            try:
                match type(component):
                    case Components.C_ATTACK:
                        if selected_type == StandardEnemy or selected_type == BossEnemy:
                            target = cast(Base.Character, target)
                            # seperate funktion für die veränderung von attack
                            attack = int(self.attack_modifiers(component.value, components)) - int(target.get_effect(Effects.SharedDebuffs.Dexterity))
                            target.damage(attack)
                            pass
                    case Components.C_DEFENSE:
                        if selected_type == PlayerCharacter:
                            # def is missing for the charakter
                            print(component.value)
                            target.increase_shield(int(component.value))
                            pass
                    case Components.C_DEFENSE_STAY:
                        # still no def i could reference
                        pass
                    case Components.C_EXHAUST_PLAYED:
                        # Exhaust every card played from the value typ
                        pass
                    case Components.C_EXHAUST_TO_HAND_CHOOSE:
                        # choose one exhausted card and add it to the hand
                        # need access to the exhaust pile and hand
                        pass
                    case Components.C_EXHAUST_TO_HAND:
                        # add this exhausted card to the hand
                        # check the current played card and add to hand
                        pass
                    case Components.C_EXHAUST_DEF:
                        # for ervery exhausted card gain value def
                        # get number exhausted cards mult value with number cards
                        pass
                    case Components.C_EXHAUST_HAND_NOATTACK:
                        # exhaust all non attack type cards in the hand
                        # check the hand for the no attack cards
                        pass
                    case Components.C_EXHAUST_HAND_ALL:
                        # exhaust all hand cards
                        pass
                    case Components.C_EXHAUST_HAND_RANDOM:
                        # exhaust one card random in the hand
                        pass
                    case Components.C_EXHAUST_HAND:
                        # choose one hand card to exhaust
                        pass
                    case Components.C_EXHAUST:
                        # add card to the exhaust pile
                        pass
                    case Components.C_DAMAGE_DEF:
                        if selected_type == StandardEnemy:
                            # get current def
                            # attack = self. - target.effect["BLOCK"]
                            # target.health_points -= attack
                            pass
                        pass
                    case Components.C_DAMAGE:
                        # player gets damage for the value, but block can reduce it
                        pass
                    case Components.C_COPY_SAME_DP:
                        # copy this card and add it to the discard pile
                        pass
                    case Components.C_COPY_TO_HAND:
                        # copy a card to the hand
                        # will be removed after the combat round
                        pass
                    case Components.C_DRAW_RANDOM_ATTACK:
                        # get random attack type card and let it cost the value
                        pass
                    case Components.C_DRAW:
                        # draw value number of cards
                        pass
                    case Components.C_GAIN_HP:
                        if selected_type == PlayerCharacter:
                            target.set_health += component.value
                        pass
                    case Components.C_GAIN_MANA:
                        if selected_type == PlayerCharacter:
                            target.set_mana += component.value
                        pass
                    case Components.C_LOSE_HP:
                        if selected_type == PlayerCharacter:
                            target.set_health -= component.value
                        pass
                    case Components.C_LOSE_MANA:
                        if selected_type == PlayerCharacter:
                            target.set_mana -= component.value
                        pass
                    case Components.C_ETHEREAL:
                        # card not played at the end of the round add it to exhaust pile
                        pass
                    case Components.C_UNPLAYABLE:
                        # card not playable
                        pass
                    case Components.C_INNATE:
                        # first combat round has this card in the hand
                        pass
                    case Components.C_ROUND:
                        # the next effect happends in the next round
                        pass
                    case Components.C_END_TURN:
                        # the next effect happends at the end of the turn
                        pass
                    case Components.C_NO_DRAW:
                        # player can't draw more cards this turn
                        # could be a status effect
                        pass
                    case Components.C_CARD_LIMIT:
                        # only value number of cards can be played
                        pass
                    case Components.C_UPGARDE_COMBAT:
                        # upgarde a card for the current fight only
                        pass
                    case Components.C_UPGARDE_NOLIMIT:
                        # card can be upgraded multiply times
                        pass
                    case Components.C_UPGRADE:
                        # upgared a card
                        pass
                    case Components.C_SKILL_FREE:
                        # card type skill costs zero this turn
                        pass
                    case Components.C_NEXT_ATTACK_TWICE:
                        # next attack card will be played twice
                        pass
                    case Components.C_DP_DWP:
                        # put a number of cards from the discard pile to the draw pile. 
                        # player chooses the cards
                        #get the discard pile and add them to draw pile
                        pass
                    case Components.C_ADD_DWP:
                        # add a (value) number of specific (name) status cards to the draw pile
                        pass
                    case Components.C_PLAY_DWP_EX:
                        # play value number of cards from drawpile and add them to exhaust pile
                        pass
                    case Components.C_COST_RED:
                        # cost to play the card will be reduced (value each time) by the number of attacked the player got in this combat
                        pass
                    case Components.C_HANDCARD_NUMBER_DAMAGE:
                        # get number of hand cards
                        # lose value number of HP per card
                        pass
                    case Components.C_DEBUFF_ALL:
                        if selected_type == StandardEnemy:
                            # add buff/debuff to all enemy. value = buff name. round = number of rounds it stays
                            pass
                    case Components.C_DEBUFF:
                        if selected_type == StandardEnemy:
                            # add buff/debuff to enemy. value = buff name. round = number of rounds it stays
                            pass
                    case Components.C_BUFF:
                        if selected_type == PlayerCharacter:
                            # add buff/debuff to the player. value = buff name. round = number of rounds it stays
                            pass
                    case Components.C_WHEN_CURSE_OR_STATUS:
                        # When the drawn card is a status or curse card
                        pass
                    case Components.C_WHEN_CURSE:
                        # when the drawn card is a curse card
                        pass
                    case Components.C_WHEN_STATUS:
                        # when the drawn card is a status card
                        pass
                    case Components.C_WHEN_EXHAUST_DRAW:
                        # when an exhausted card gets drawn. Draw a number of cards
                        pass
                    case Components.C_WHEN_EXHAUST_CARD:
                        # when a card gets exhausted. Do the next effects
                        pass
                    case Components.C_WHEN_EXHAUST:
                        # when this card gets exhausted
                        pass
                    case Components.C_WHEN_BUFF:
                        # when the player has the (value) named effect
                        pass
                    case Components.C_WHEN_DEBUFF:
                        # when the enemy has the (value) named effect
                        pass
                    case Components.C_WHEN_ONLY:
                        # when the hand cards only have cards from the (value) named typ in it
                        pass
                    case Components.C_WHEN_ATTACKED:
                        # when the player gets attacked in this turn
                        pass
                    case Components.C_WHEN_NOT_PLAYED:
                        # when this card is not played
                        pass
                    case Components.C_WHEN_DRAWN:
                        # when this card is drawn
                        pass
                    case Components.C_WHEN_OTHER_CARDPLAYED:
                        # when other cards are played
                        pass
                    case Components.C_WHEN_REMOVED:
                        # when the card is removed from the deck
                        pass
                    case Components.C_WHEN_TYPE:
                        # when cards from the (value) named typ are played
                        pass
                    case Components.C_WHEN_INCOMING:
                        # when the enemy will attack next round
                        pass
                    case Components.C_WHEN_LOSE_HP_CARD:
                        # when the player loses HP by a card effect
                        pass
                    case Components.C_WHEN_DEF:
                        # when the def of the player gets raised
                        pass
            except AttributeError as e:
                print("[ECSOContext][CARDSYSTEM]", e)
                return False
            except TypeError as e:
                print("[ECSOContext][CARDSYSTEM]", e)
                return False
        return True
