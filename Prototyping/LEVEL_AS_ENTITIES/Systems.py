from components import position

class Systems():
    @staticmethod
    def translation_system(current_position: tuple, translation: tuple, position_component: position):
        position_component.x = current_position[0] + translation[0]
        position_component.y = current_position[1] + translation[1]
        position_component.z = current_position[2] + translation[2]
