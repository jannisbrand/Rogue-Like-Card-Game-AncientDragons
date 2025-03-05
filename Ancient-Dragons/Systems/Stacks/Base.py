from random import randint


class CardStack():
    def __init__(self, context_id: int):
        self.context_id = context_id
        self.cards: list[int] = []

    def get_cards(self) -> list[int]:
        try:
            return self.cards.copy()
        except AttributeError as e:
            print("[CARDSTACK]", e)

    def shuffle(self, times: int):
        print("[CARDSTACK][SHUFFLE] Before:", self.cards)
        for _ in range(times):
            random_index_1 = randint(0, len(self.cards) - 1)
            random_index_2 = randint(0, len(self.cards) - 1)
            temporary_id = self.cards[random_index_1]
            self.cards[random_index_1] = self.cards[random_index_2]
            self.cards[random_index_2] = temporary_id
        print("[CARDSTACK][SHUFFLE] After:", self.cards)

    def add_card(self, card: int):
        try:
            self.cards.append(card)
        except AttributeError as e:
            print("[CARDSTACK]", e)

    def take_card(self) -> int:
        """Removes the top card from the stack
        """
        try:
            return self.cards.pop(len(self.cards) - 1)
        except AttributeError as e:
            print("[CARDSTACK]", e)
