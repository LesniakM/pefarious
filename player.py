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

    def place_spy(self):
        if self.spies[0] > 0:
            while self.selected_spy_place == 0:
                a = input(f"{self.name}, where do you want to place a spy?\n 1 - Spy, 2 - Construct, 3 - Research, 4 - Work\n")
                if 1 <= int(a) <= 4:
                    self.selected_spy_place = int(a)
                    if self.money >= self.game.spy_cost[self.selected_spy_place]:
                        self.spies[self.selected_spy_place] += 1
                        self.spies[0] -= 1
                        self.money -= self.game.spy_cost[self.selected_spy_place]
                        print(f"{self.name} placed a spy.")
                    else:
                        print(f"{self.name} You don't have enough money and lose this round.")
                    break
        else:
            print(f"{self.name}, you don't have any remaining spies and you lost this turn.")

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
        if self.invention_cards:
            for index, card in enumerate(self.invention_cards):
                print(f"Type '{index+1}' for: {card.name.ljust(30)} cost: {str(card.cost).rjust(2)}, WP: {card.wp}")
            self.selected_invention_card = int(input("\n"))-1
            self.construct(self.invention_cards[self.selected_invention_card])
        else:
            print(f"{self.name}, you don't have invention card and you lost this turn.")

    def construct(self, card: Card):
        cost = card.cost
        name = card.name
        wp = card.wp
        if self.money >= cost:
            print(f"Card {name} was constructed successfully!")
            print(f"{self.name} earns {wp} win points!")
            self.change_money(-cost)
            self.inventions.append(card)
            self.invention_cards.remove(card)
            self.update_win_points()
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
    def __init__(self, g, name):
        super().__init__(g, f"{name} Bot")

    def select_action(self):
        self.selected_action = self.game.round_index % 4 + 1
        print(f"{self.name} selected action {self.selected_action}")
    
    def place_spy(self):
        if self.spies[0] > 0:
            # work in progress
            # section below must be checked for money !!
            self.selected_spy_place = 2

            # duplicate from Player
            self.spies[self.selected_spy_place] += 1
            self.spies[0] -= 1
            self.money -= self.game.spy_cost[self.selected_spy_place]

            print(f"{self.name} selected spy place at {self.selected_action}")

    def choose_card_to_construct(self):
        print(f"{self.name} is constructing...")
        if len(self.invention_cards) > 0:
            cheapest = sorted(self.invention_cards, key=lambda c: c[1][2])[0]
            if cheapest[1][2] <= self.money:
                self.construct(cheapest)
