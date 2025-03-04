from GUI.Interactibles.Base import InteractibleSprite


class InteractibleEnvironmental(InteractibleSprite):
    def __init__(self, context_id, type_id, reference_rect, name, color, width, height, image_path=""):
        super().__init__(context_id, type_id, reference_rect, name, color, width, height, image_path)
        # Could later have animations; iterable sprites for animations; ...
        pass
