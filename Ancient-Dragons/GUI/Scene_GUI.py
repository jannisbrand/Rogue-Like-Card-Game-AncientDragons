from GUI.BaseGUI import BaseGUI


class SceneGUI(BaseGUI):
    def __init__(self, context_id, type_id, reference_rect, name, color, width, height, image_path=""):
        super().__init__(context_id, type_id, reference_rect, name, color, width, height, image_path)
