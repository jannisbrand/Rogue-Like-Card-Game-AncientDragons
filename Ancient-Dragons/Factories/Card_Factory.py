import sqlite3
from typing import Any
from Characters.Base import Character
from Characters.Player_Character import PlayerCharacter
from ECSO_Context import ECSO_Context
from Components import Components


class CardFactory():
    def __init__(self, application, renderer, ecso_context: "ECSO_Context", database_path: str = "Ancient-Dragons_Database.db"):
        # ### Database ### #
        self.application = application
        self.renderer = renderer
        self.database_connection = sqlite3.connect(database_path)
        # ### Database ### #

        self.ecso_context = ecso_context
        
        # Card name: {}
        #   Component:
        #       value = x
        #   Component:
        #       value = x
        self.temp_card_blueprint: dict[str, dict[str, int]] = {}
        self.temp_card_blueprint["TEST_CARD"] = {}
        self.temp_card_blueprint["TEST_CARD"]["ATTACK"] = 5
        self.temp_card_blueprint["TEST_CARD"]["DEFENSE"] = 2

        # ### Factory ### #
        self.fabrication_process = {
            "Name": self.handle_name,
            "Type_ID": self.handle_type,
            "Charakter_ID": self.handle_character_affiliation,
            "Cost": self.handle_cost,
            "Text": self.handle_text,
            "Effect": self.handle_effects,
            "Path_Picture": self.handle_image_path,
        }

    def get_database_column_names(self, table: str) -> list[str]:
        table_info = self.database_connection.cursor().execute(f"PRAGMA table_info({table})")
        column_names = list()
        for column in table_info:
            column_name = column[1]
            column_names.append(column_name)
        return column_names

    def fabricate_all(self):
        card_collection = self.database_connection.cursor().execute("SELECT * FROM Cards")
        column_names = self.get_database_column_names("Cards")
        for card_data in card_collection.fetchall():
            # PATTERN
            # CARD ID; CARD NAME; CHARACTER TYPE ID; CHARACTER ID; CARD COST; CARD TEXT; CARD EFFECTS; CARD IMAGE PATH
            if len(card_data) != len(column_names):
                print("[ECFactory] Card data and Colum names do not match!")
                continue
            print("[ECFactory] Card data: " + str(card_data))
            self.parse_card(column_names, card_data)

    def parse_card(self, column_names: list[str], card_data: tuple[int, str, int, int, int, str, str, str]) -> bool:
        """Routes data to further processing

        Args:
            card_data (tuple[int, str, int, int, int, str, str, str])

        Returns:
            bool: True if no error occured.
        """
        card_entity = self.ecso_context.add_entity()  # Creates a new entity in the context
        index = 0
        for data in card_data:
            try:
                if column_names[index] != "ID":
                    handler = self.fabrication_process[column_names[index]]
                    if column_names[index] == "Charakter_ID":
                        created_components = handler(card_data[3], data)  # Only the handler-methond for the character id has two arguments
                        if created_components is None:
                            index += 1
                            continue
                    else:
                        created_components = handler(data)  # Whacky solution | Could be a single object or a list of objects

                    if isinstance(created_components, list):  # Check if its a list of objects
                        # if index == 6 or index == 1:  # Temp
                        self.ecso_context.add_components(card_entity, created_components)
                    else:
                        # if index == 6 or index == 1:  # Temp
                        self.ecso_context.add_component(card_entity, created_components)
                    print("[ECFactory] Created components: ", created_components)  # Names appear seperated bc strings are being casted to type l==t.. Temporaryly
            except KeyError as e:
                print(f"[ECFactory] Key not found: {e}")
            except TypeError as e:
                print(f"[ECFactory] Handler returned invalid type: {e}")
            index += 1

        return True
    
    def handle_name(self, value: str = "") -> Any:
        component = Components.C_DISPLAY_NAME(value)
        return component

    def handle_type(self, value: int = -1) -> Any:
        # TODO: Get type name from table "Types"
        component = Components.C_CARD_TYPE()
        return component

    def handle_character_affiliation(self, character_id: int, value: int) -> Any:
        # TODO: Implementation of a character factory first..
        if character_id is not None:
            character_name = self.database_connection.cursor().execute(f"SELECT Name FROM Charakters WHERE ID = {character_id}").fetchall()[0][0]
            character_objects = self.ecso_context.get_game_objects_of_type(PlayerCharacter)
            for entity, game_object in character_objects:
                if game_object.name == character_name:
                    return Components.C_CHARACTER_AFFILIATION(entity) # ID here
        else:
            return None

    def handle_cost(self, value: int) -> Any:
        component = Components.C_CARD_COSTS(value)
        return component

    def handle_text(self, value: str) -> Any:
        component = Components.C_DISPLAY_TEXT(value)
        return component

    def handle_effects(self, value: str):   # TODO: Return value should be a tuple.. :)
        # TODO: Addition of all effekt components :')
        # TODO: Seperate sub effects eg.: ATK_RANDOM; ATK_ALL   (All different components)
        list_of_effects = []
        seperated_string = value.split("|")
        effect = seperated_string[0]
        while effect is not None:
            # Attack effects
            seperated_effect = effect.split("_")
            if effect.startswith("ATK"):
                if seperated_effect[1] == "ALL":
                    component = Components.C_ATTACK_ALL()
                elif seperated_effect[1] == "RANDOM":
                    component = Components.C_ATTACK_RANDOM()
                elif seperated_effect[1] == "NUM":
                    component = Components.C_ATTACK_NUM(seperated_effect[2])
                elif seperated_effect[0] == "ATK+":
                    component = Components.C_ATTACK_PLUS(seperated_effect[1], seperated_effect[3])
                elif seperated_effect[0] == "ATKINCREASE":
                    component = Components.C_ATTACK_INCREASE(seperated_effect[1])
                elif seperated_effect[0] == "ATKMULT":
                    component = Components.C_ATTACK_MULT(seperated_effect[1])
                else:
                    component = Components.C_ATTACK(seperated_effect[1])
                    
            # Defense effects
            elif effect.startswith("DEF_"):
                if seperated_effect[1] == "STAY":
                    component = Components.C_DEFENSE_STAY()
                else:
                    component = Components.C_DEFENSE(seperated_effect[1])

            # Exhaust effects
            elif effect.startswith("EX"):
                if len(seperated_effect) != 1:
                    if seperated_effect[1] == "PLAYED":
                        component = Components.C_EXHAUST_PLAYED(seperated_effect[2])
                    elif seperated_effect[1] == "TO":
                        if len(seperated_effect) == 4:
                            if seperated_effect[3] == "CHOOSE":
                                component = Components.C_EXHAUST_TO_HAND_CHOOSE()
                        else:
                            component = Components.C_EXHAUST_TO_HAND()
                    elif seperated_effect[1] == "ATK":
                        component = Components.C_EXHAUST_ATK(seperated_effect[2])
                    elif seperated_effect[1] == "DEF":
                        component = Components.C_EXHAUST_DEF(seperated_effect[2])
                    elif seperated_effect[1] == "HAND":
                        if len(seperated_effect) == 3:
                            if seperated_effect[2] == "NOATTACK":
                                component = Components.C_EXHAUST_HAND_NOATTACK()
                            elif seperated_effect[2] == "ALL":
                                component = Components.C_EXHAUST_HAND_ALL()
                            elif seperated_effect[2] == "RANDOM":
                                component = Components.C_EXHAUST_HAND_RANDOM()
                        else:
                            component = Components.C_EXHAUST_HAND()
                else:
                    component = Components.C_EXHAUST()

            # other effects
            elif effect.startswith("DAMAGE_"):
                if seperated_effect[1] == "DEF":
                    component = Components.C_DAMAGE_DEF()
                else:
                    component= Components.C_DAMAGE(seperated_effect[1])

            elif effect.startswith("COPY_"):
                if seperated_effect[1] == "SAME":
                    component = Components.C_COPY_SAME_DP()
                elif seperated_effect[1] == "TO":
                    component = Components.C_COPY_TO_HAND()

            elif effect.startswith("DRAW_"):
                if seperated_effect[1] == "RANDOM":
                    component = Components.C_DRAW_RANDOM_ATTACK(seperated_effect[3])
                else:
                    component = Components.C_DRAW(seperated_effect[1])

            elif effect.startswith("GAIN"):
                if seperated_effect[1] == "HP":
                    component = Components.C_GAIN_HP(seperated_effect[2])
                if seperated_effect[1] == "MANA":
                    component = Components.C_GAIN_MANA(seperated_effect[2])

            elif effect.startswith("LOSE"):
                if seperated_effect[1] == "HP":
                    component = Components.C_LOSE_HP(seperated_effect[2])
                if seperated_effect[1] == "MANA":
                    component = Components.C_LOSE_MANA(seperated_effect[2])

            elif effect.startswith("ETHEREAL"):
                component = Components.C_ETHEREAL()

            elif effect.startswith("UNPLAYABLE"):
                component = Components.C_UNPLAYABLE()

            elif effect.startswith("INNATE"):
                component = Components.C_INNATE()

            elif effect.startswith("ROUND"):
                component = Components.C_ROUND()

            elif effect.startswith("END"):
                component = Components.C_END_TURN()

            elif effect.startswith("NO"):
                component = Components.C_NO_DRAW()

            elif effect.startswith("CARD"):
                component = Components.C_CARD_LIMIT(seperated_effect[2])

            elif effect.startswith("UPGRADE"):
                if seperated_effect[1] == "COMBAT":
                    component = Components.C_UPGARDE_COMBAT()
                elif seperated_effect[1] == "NOLIMIT":
                    component = Components.C_UPGARDE_NOLIMIT()
                else:
                    component = Components.C_UPGRADE()

            elif effect.startswith("SKILL"):
                component = Components.C_SKILL_FREE()

            elif effect.startswith("NEXT"):
                component = Components.C_NEXT_ATTACK_TWICE()

            elif effect.startswith("DP"):
                component = Components.C_DP_DWP(seperated_effect[2])

            elif effect.startswith("ADD"):
                component = Components.C_ADD_DWP(seperated_effect[1], seperated_effect[2])

            elif effect.startswith("PLAY"):
                component = Components.C_PLAY_DWP_EX(seperated_effect[1])

            elif effect.startswith("COST"):
                component = Components.C_COST_RED(seperated_effect[2])

            elif effect.startswith("HANDCARD"):
                component = Components.C_HANDCARD_NUMBER_DAMAGE(seperated_effect[3])

            elif effect.startswith("KILL_GAIN"):
                if seperated_effect[2] == "HP":
                    component = Components.C_GAIN_HP(seperated_effect[3])
                elif seperated_effect[2] == "MANA":
                    component = Components.C_GAIN_MANA(seperated_effect[3])

            elif effect.startswith("DB"):
                if seperated_effect[0] == "DBALL":
                    component = Components.C_DEBUFF_ALL(seperated_effect[1], seperated_effect[2])
                else:
                    component = Components.C_DEBUFF(seperated_effect[1], seperated_effect[2])

            elif effect.startswith("B"):
                component = Components.C_BUFF(seperated_effect[1], seperated_effect[2])

            # conditions
            elif effect.startswith("WHEN"):
                if seperated_effect[1] == "CURSE":
                    if len(seperated_effect) == 4:
                        if seperated_effect[3] == "STATUS":
                            component = Components.C_WHEN_CURSE_OR_STATUS()
                    else:
                        component = Components.C_WHEN_CURSE()
                elif seperated_effect[1] == "STATUS":
                    component = Components.C_WHEN_STATUS()

                elif seperated_effect[1] == "EX":
                    if len(seperated_effect) == 3:
                        if seperated_effect[2] == "DRAW":
                            component = Components.C_WHEN_EXHAUST_DRAW(seperated_effect[3])
                        elif seperated_effect[2] == "CARD":
                            component = Components.C_WHEN_EXHAUST_CARD()
                    else:
                        component = Components.C_WHEN_EXHAUST()

                elif seperated_effect[1] == "B":
                    component = Components.C_WHEN_BUFF(seperated_effect[2])
                elif seperated_effect[1] == "DB":
                    component = Components.C_WHEN_DEBUFF(seperated_effect[2])

                elif seperated_effect[1] == "ONLY":
                    component = Components.C_WHEN_ONLY(seperated_effect[2])

                elif seperated_effect[1] == "ATTACKED":
                    component = Components.C_WHEN_ATTACKED()

                elif seperated_effect[1] == "NOT":
                    component = Components.C_WHEN_NOT_PLAYED()

                elif seperated_effect[1] == "DRAWN":
                    component = Components.C_WHEN_DRAWN()
                elif seperated_effect[1] == "OTHER":
                    component = Components.C_WHEN_OTHER_CARDPLAYED()

                elif seperated_effect[1] == "REMOVED":
                    component = Components.C_WHEN_REMOVED()

                elif seperated_effect[1] == "TYPE":
                    component = Components.C_WHEN_TYPE(seperated_effect[2])

                elif seperated_effect[1] == "INCOMING":
                    component = Components.C_WHEN_INCOMING()

                elif seperated_effect[1] == "LOSE":
                    component = Components.C_WHEN_LOSE_HP_CARD()

                elif seperated_effect[1] == "DEF":
                    component = Components.C_WHEN_DEF()
            else:
                component = ""
            
            if effect != None:
                list_of_effects.append(component)
            if len(seperated_string) != 0:
                seperated_string.pop(0)
                if len(seperated_string) != 0:
                    effect = seperated_string[0]
                else:
                    effect = None
        return list_of_effects

    def handle_image_path(self, value: str) -> Any:
        component = Components.C_IMAGE_PATH()
        return component

    def copy_entity(self, entity: int) -> int:
        copy_of_components = list.copy(self.ecso_context.get_components(entity))
        new_entity = self.ecso_context.add_entity()
        self.ecso_context.add_components(new_entity, copy_of_components)
        return new_entity

    def build(self):
        entity = self.ecso_context.add_entity()
        card_keys = self.temp_card_blueprint["TEST_CARD"].keys()
        for key in card_keys:
            match key:
                case "ATTACK":
                    value = self.temp_card_blueprint["TEST_CARD"][key]
                    component = Components.C_ATTACK(value)
                case "DEFENSE":
                    value = self.temp_card_blueprint["TEST_CARD"][key]
                    component = Components.C_DEFENSE(value)
                case _:
                    continue
            self.ecso_context.add_component(entity, component)
