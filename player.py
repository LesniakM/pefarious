from cards import Card


class Player:
    def __init__(self, g, name: str):
        self.game = g
        self.name = name
        self.money = g.start_money
        self.invention_cards = []
        self.inventions = []
        self.get_invention_card(g.start_cards)
        self.win_points = 0
        self.spies = [5, 0, 0, 0, 0]  # first value represents number of spies remaining
        self.selected_action = 0
        self.selected_invention_card = 0
        self.selected_spy_place = 0

    def get_invention_card(self, amount: int) -> None:
        for i in range(amount):
            self.invention_cards.append(self.game.pick_card())

    def try_describe_invention_cards(self) -> tuple[bool, str]:
        if self.invention_cards:
            description = ""
            for index, card in enumerate(self.invention_cards):
                description += f"({index+1}): {card.name.ljust(30)} cost: {str(card.cost).rjust(2)}, WP: {card.wp}\n"
            return True, description
        else:
            return False, ""

    def change_money(self, amount: int):
        self.money = self.money + amount
        if self.money < 0:
            self.money = 0

    def select_action(self):
        while self.selected_action == 0:
            a = input(f"{self.name}, what would you like to do?\n 1 - Spy, 2 - Construct, 3 - Research, 4 - Work\n")
            if 1 <= int(a) <= 4:
                self.selected_action = int(a)
                break

    def try_place_spy(self, spy_place) -> bool:
        if self.spies[0] > 0 and self.money >= self.game.spy_cost[spy_place]:
            self.selected_spy_place = spy_place
            self.spies[self.selected_spy_place] += 1
            self.spies[0] -= 1
            self.change_money(-self.game.spy_cost[self.selected_spy_place])
            return True
        else:
            return False

    def choose_place_for_spy(self):
        print(f"{self.name}, where do you want to place a spy?\n" +
                "1 - Spy, 2 - Construct, 3 - Research, 4 - Work")
        result = int(input("\n"))
        if self.try_place_spy(result):
            print(f"{self.name} placed a spy.")
        else:
            print(f"{self.name}, you can't place a spy on this action.")

    def gather_spy_income(self, nearest_actions):
        income = 0
        for action in nearest_actions:
            income += self.game.spy_income*self.spies[action]
            if self.selected_spy_place == 1 and action == 1:
                income -= self.game.spy_income*self.spies[1]
        self.change_money(income)
        return income

    def choose_card_to_construct(self):
        print(f"{self.name}, what do you want to construct?")
        result, description =  self.try_describe_invention_cards()
        if result:
            print(description)
            self.selected_invention_card = int(input("\n"))-1
            self.construct(self.invention_cards[self.selected_invention_card])
        else:
            print(f"{self.name}, you don't have invention card and you lost this turn.")

    # assumes the card is owned by the player
    def try_construct(self, card: Card) -> bool:
        if self.money >= card.cost:
            self.change_money(-card.cost)
            self.inventions.append(card)
            self.invention_cards.remove(card)
            self.update_win_points()
            return True
        else:
            return False

    def construct(self, card: Card):
        if self.try_construct(card):
            print(f"Card {card.name} was constructed successfully!")
            print(f"{self.name} earns {card.wp} win points!")
        else:
            print(f"You don't have enough money and lose this round.")

    def update_win_points(self):
        self.win_points = sum([card.wp for card in self.inventions])


class Bot(Player):
    """
        Proof of concept only
        Player needs some refactoring to do it properly
        Abstract away from Player methods for: money checks, try/check spy placement
        Bot is able to construct fake card !!
    """
    def __init__(self, g, name: str):
        super().__init__(g, f"{name} Bot")

    def select_action(self) -> None:
        self.selected_action = self.game.round_index % 4 + 1
        print(f"{self.name} selected action {self.selected_action}")
    
    def choose_place_for_spy(self) -> None:
        if self.try_place_spy(2):
            print(f"{self.name} selected spy place at {self.selected_action}")
        else:
            print(f"{self.name} failed at choosing the place for a spy")

    def choose_card_to_construct(self) -> None:
        cheapest = sorted(self.invention_cards, key=lambda c: c.cost)[0]

        card = cheapest
        if self.try_construct(cheapest):
            print(f"Card {card.name} was constructed successfully!")
            print(f"{self.name} earns {card.wp} win points!")
        else:
            print(f"{self.name} doesn't construct anything this round")
