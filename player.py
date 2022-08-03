class Player:
    def __init__(self, g, name):
        self.game = g
        self.name = name
        self.money = g.start_money
        self.pick_random_card = g.pick_random_card
        self.invention_cards = []
        self.inventions = []
        self.get_invention_card(g.start_cards)
        self.win_points = 0
        self.spies = [5, 0, 0, 0, 0] # first value represents number of spies remaining
        self.selected_action = 0
        self.selected_invention_card = 0
        self.selected_spy_place = 0

    def get_invention_card(self, amount):
        for i in range(amount):
            self.invention_cards.append(self.pick_random_card())

    def select_action(self):
        while self.selected_action == 0:
            a = input(f"{self.name}, what would you like to do?\n 1 - Spy, 2 - Construct, 3 - Research, 4 - Work\n")
            if 1 <= int(a) <= 4:
                self.selected_action = int(a)
                break

    def change_money(self, amount):
        self.money = self.money + amount
        if self.money < 0:
            self.money = 0

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
                print(f"Type '{index+1}' for: {card[1][1].ljust(30)} cost: {str(card[1][2]).rjust(2)}, WP: {card[1][3]}")
            self.selected_invention_card = int(input("\n"))-1
            self.construct(self.invention_cards[self.selected_invention_card])
        else:
            print(f"{self.name}, you don't have invention card and you lost this turn.")

    def construct(self, card):
        cost = card[1][2]
        name = card[1][1]
        wp = card[1][3]
        if self.money >= cost:
            print(f"Card {name} was constructed successfully!")
            print(f"{self.name} earns {wp} win points!")
            self.win_points = self.win_points + wp
            self.change_money(-cost)
            self.invention_cards.remove(card)
            self.inventions.append(name)
        else:
            print(f"You don't have enough money and lose this round.")


# class Bot(Player):