import unittest
from ECSO_Context import ECSO_Context


class TestECSOContext(unittest.TestCase):

    def setUp(self):
        self.context = ECSO_Context()

    def test_add_entity(self):
        entity_id = self.context.add_entity()
        self.assertIn(entity_id, self.context.entities)
        self.assertEqual(entity_id, 1)  # Erste Entität sollte ID 1 haben

    def test_add_component(self):
        class Position:
            def __init__(self, x, y):
                self.x = x
                self.y = y

        entity = self.context.add_entity()
        position = Position(10, 20)
        self.context.add_component(entity, position)

        retrieved_component = self.context.get_component(entity, Position)
        self.assertIsNotNone(retrieved_component)
        self.assertEqual(retrieved_component.x, 10)
        self.assertEqual(retrieved_component.y, 20)

    def test_add_game_object(self):
        class GameObject:
            def __init__(self, name):
                self.name = name

        entity = self.context.add_entity()
        game_object = GameObject("Player")
        self.context.add_game_object(entity, game_object)

        retrieved_object = self.context.get_game_object(entity, GameObject)
        self.assertIsNotNone(retrieved_object)
        self.assertEqual(retrieved_object.name, "Player")

    def test_remove_game_object(self):
        class GameObject:
            def __init__(self, name):
                self.name = name

        entity = self.context.add_entity()
        game_object = GameObject("Enemy")
        self.context.add_game_object(entity, game_object)

        self.context.remove_game_object(entity)
        self.assertIsNone(self.context.get_game_object(entity, GameObject))


if __name__ == '__main__':
    unittest.main()
