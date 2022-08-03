from random import randint

from player import Player

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
        self.spy_cost = [0, 0, 2, 0, 1] # indexed with actions
        self.start_money = 10
        self.start_cards = 3
        self.points_to_win = 20       
        self.round_index = 0
        self.add_players(players)
        self.start_game()

    def pick_random_card(self):
        card_ids = list(self.invention_cards.keys())[1:]
        deck_has_cards = 0
        for card_id in card_ids:
            if self.invention_cards[card_id][0] == 1:
                deck_has_cards = 1
        while deck_has_cards:
            picked = randint(0, len(card_ids)-1)
            if self.invention_cards[card_ids[picked]][0] == 1:
                self.invention_cards[card_ids[picked]][0] = 0
                card = self.invention_cards[card_ids[picked]]
                print(f"Picked {card_ids[picked]}: {card[1].ljust(30)} cost: {str(card[2]).rjust(2)}, WP: {card[3]}")
                return [card_ids[picked], self.invention_cards[card_ids[picked]]]
        print("Deck is empty! No card were picked this time.")

    def add_players(self, amount):
        for player in range(amount):
            name = input("Provide player name: ")
            self.players.append(Player(self, name))

    # used for calculating spy income
    def get_nearest_players(self, index):
        if len(self.players) <= 3:
            return self.players[0:index]+self.players[index+1:]

    def start_round(self):
        print(f"\nRound {self.round_index} starts.")
        print("\n".join([f""
                         f"{player.name} has {player.money} gold coins, {player.win_points} win-points and "
                         f"{len(player.invention_cards)} invention cards\n"
                         f"{player.name}'s spies sit like this {player.spies[1:5]}\n" for player in self.players]))
        for player in self.players:
            player.select_action()
        print()

    def spy_stage(self):
        for player in self.players:
            if player.selected_action == 1:
                print(f"{player.name} is spying")
                player.place_spy()

    def spy_income_stage(self):
        for index, player in enumerate(self.players):
            nearest_actions = [p.selected_action for p in self.get_nearest_players(index)]
            income = player.gather_spy_income(nearest_actions)
            print(f"{player.name} earned {income} gold coins from spies")

    def construct_stage(self):
        for player in self.players:
            if player.selected_action == 2:
                print(f"{player.name} is constructing")
                player.choose_card_to_construct()

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
            player.selected_spy_place = 0
            if player.win_points >= self.points_to_win:
                self.winner = player.name

    def start_game(self):
        print("""Game is starting! \n""")
        while not self.winner:
            self.start_round()
            self.spy_stage()
            self.spy_income_stage()
            self.construct_stage()
            self.research_stage()
            self.work_stage()
            self.end_round()
            self.round_index = self.round_index + 1
        print(f"{self.winner} has won the game!")