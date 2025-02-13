from ESC_Context import ECS_Context
from Components import Components


class CardFactory():
    def __init__(self, ecs_context: "ECS_Context"):   
        self.context = ecs_context
        
        # Card name: {}
        #   Component:
        #       value = x
        #   Component:
        #       value = x
        self.temp_card_blueprint: dict[str, dict[str, int]] = {}
        self.temp_card_blueprint["TEST_CARD"] = {}
        self.temp_card_blueprint["TEST_CARD"]["ATTACK"] = 5
        self.temp_card_blueprint["TEST_CARD"]["DEFENSE"] = 2

    def build(self):
        entity = self.context.add_entity()
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
            self.context.add_component(entity, component)
