from random import randint


class Game:
    def __init__(self, players):
        self.players = []
        self.winner = ""
        # ID : (AVAILABILITY, NAME, COST, WINPOINTS, (EFFECT1), (EFFECT2))
        self.invention_cards = {00: [0, "N", "C", "WP", ("TARGET", "TYPE", "AMOUNT"), ("TARGET", "TYPE", "AMOUNT")],
                                12: [1, "Uzależniająca gra", 0, 1, ("Personal", "Cash", 4)],
                                13: [1, "Cybernetyczne zwierzątko", 0, 1, ("Personal", "card", 1, "cash", 2)],
                                14: [1, "Maszyna PKiKzM", 0, 2],
                                18: [1, "Urządzenie maskujące", 4, 3],
                                19: [1, "Afrodyzjaki", 7, 2, ("Personal", "Cash", 8)],
                                27: [1, "Zabójcze pszczoły", 8, 4],
                                28: [1, "Plaga szarańczy", 8, 4],
                                42: [1, "Generator trzesień ziemi", 12, 5],
                                43: [1, "Generator huraganów", 12, 5],
                                44: [1, "Zamrażacz pokrywy lodowej", 12, 5],
                                47: [1, "Generator fal pływowych", 12, 5],
                                48: [1, "Wyzwalacz wulkanów", 12, 5],
                                54: [1, "Wytwornica śniegu", 16, 6],
                                55: [1, "Wielka orbitalna asteroida", 16, 6],
                                56: [1, "Grawitacja czarnej dziury", 16, 6],
                                57: [1, "Promienie śmierci", 16, 6],
                                58: [1, "Potwór z głębin", 16, 6],
                                59: [1, "Reduktor ozonu", 16, 6]}
        self.work_income = 4
        self.research_income = 2
        self.research_cards = 1
        self.spy_income = 1
        self.round_index = 0

        self.add_players(2)
        self.start_game()

    def pick_random_card(self):
        card_ids = list(self.invention_cards.keys())[1:]
        while 1:
            picked = randint(0, len(card_ids)-1)
            if self.invention_cards[card_ids[picked]][0] == 1:
                self.invention_cards[card_ids[picked]][0] = 0
                card = self.invention_cards[card_ids[picked]]
                print(f"Picked {card_ids[picked]}: {card[1].ljust(30)} cost: {str(card[2]).rjust(2)}, WP: {card[3]}")
                return [card_ids[picked], self.invention_cards[card_ids[picked]]]

    def add_players(self, amount):
        for player in range(amount):
            name = input("Provide player name: ")
            self.players.append(Player(self, 10, 3, name, self.pick_random_card))

    def start_round(self):
        print(f"\nRound {self.round_index} starts.")
        print("\n".join([f""
                         f"{player.name} has {player.money} gold coins, {player.win_points} win-points and "
                         f"{len(player.invention_cards)} invention cards" for player in self.players]))
        for player in self.players:
            player.select_action()
        print()

    def spy_stage(self):
        for player in self.players:
            if player.selected_action == 1:
                print(f"{player.name} is spying")
                player.place_spy()

    def construct_stage(self):
        for player in self.players:
            if player.selected_action == 2:
                print(f"{player.name} is constructing")
                player.construct()

    def research_stage(self):
        for player in self.players:
            if player.selected_action == 3:
                cards = self.research_cards
                income = self.research_income
                print(f"{player.name} get {cards} card and {income} coins by doing research")
                player.get_invention_card(cards)
                player.change_money(self.research_income)

    def work_stage(self):
        for player in self.players:
            if player.selected_action == 4:
                income = self.work_income
                print(f"{player.name} earned {income} coins by working")
                player.change_money(income)

    def end_round(self):
        for player in self.players:
            player.selected_action = 0

    def start_game(self):
        while not self.winner:
            self.start_round()
            self.spy_stage()
            self.construct_stage()
            self.research_stage()
            self.work_stage()
            self.end_round()
            self.round_index = self.round_index + 1


class Player:
    def __init__(self, g, money, cards, name, pick_card):
        self.game = g
        self.name = name
        self.money = money
        self.pick_random_card = pick_card
        self.invention_cards = []
        self.get_invention_card(cards)
        self.win_points = 0
        self.selected_action = 0

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
        input("Where you want to place a spy?\n 1 - Spy, 2 - Construct, 3 - Research, 4 - Work\n")

    def construct(self):
        input("What you want to construct?\n <cards will be displayed here>\n")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    game = Game(2)
