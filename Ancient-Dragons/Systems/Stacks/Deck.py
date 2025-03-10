from Systems.Stacks.Base import CardStack


class Deck(CardStack):
    def __init__(self, context_id):
        super().__init__(context_id)
