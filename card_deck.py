from cards import card_parser, Card, invention_cards_data
from collections import deque
from random import shuffle


class CardDeck:
    def __init__(self):
        self.card_stack = deque()
        self.rejected_card_stack = deque()

        # Make cards and shuffle them. GC will delete card_objs list after CardDeck init.
        card_objs = [card_parser(card_id, invention_cards_data[card_id]) for card_id in invention_cards_data.keys()]
        card_objs.pop(0)  # Remove template card
        shuffle(card_objs)
        for card in card_objs:
            self.card_stack.append(card)

    def get_card(self) -> Card or None:
        if self.card_stack:
            return self.card_stack.pop()
        else:
            self.reuse_rejected_cards()
            if self.card_stack:
                return self.card_stack.pop()
            else:
                print("No more cards on board")
                return None

    def reject_card(self, card: Card) -> None:
        self.rejected_card_stack.appendleft(card)  # append left coz we want FiFo here.

    def reuse_rejected_cards(self) -> None:
        self.card_stack = self.rejected_card_stack
        self.rejected_card_stack.clear()
