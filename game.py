from random import randint
from player import Player, Bot
from card_deck import CardDeck
from cards import Card


class Game:
    def __init__(self, players: int):
        self.players = []
        self.winner = ""
        self.card_deck = CardDeck()
        self.work_income = 4
        self.research_income = 2
        self.research_cards = 1
        self.spy_income = 1
        self.spy_cost = ("_", 0, 2, 0, 1)  # indexed with actions
        self.start_money = 10
        self.start_cards = 3
        self.points_to_win = 20
        self.round_index = 0
        self.add_players(players)
        self.start_game()

    def pick_card(self) -> Card:
        return self.card_deck.get_card()

    def add_players(self, amount: int) -> None:
        for player in range(amount):
            name = input("Provide player name: ")
            self.players.append(Player(self, name))

    def add_bots(self, amount: int) -> None:
        for player in range(amount):
            self.players.append(Bot(self, "#1"))

    # used for calculating spy income
    def get_nearest_players(self, index: int) -> list[Player]:
        if len(self.players) <= 3:
            return self.players[0:index] + self.players[index + 1:]

    def start_round(self) -> None:
        print(f"\nRound {self.round_index} starts.")
        print("\n".join([f""
                         f"{player.name} has {player.money} gold coins, {player.win_points} win-points and "
                         f"{len(player.invention_cards)} invention cards\n"
                         f"{player.name}'s spies sit like this {player.spies[1:5]}\n" for player in self.players]))
        for player in self.players:
            player.select_action()
        print()

    def spy_stage(self) -> None:
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

    def data_validation(self) -> None:
        """
        This method will check if there's any illegal value in game/player data.
        It's mainly for bug highlighting.
        """
        for player in self.players:
            assert sum([spy for spy in player.spies]) == 5, f"Illegal total spy amount! {player}: {player.spies}"
            assert sum([0 <= spy <= 5 for spy in player.spies]) == 5, f"Illegal spies! {player}: {player.spies}"
            assert player.money >= 0, f"Negative amount of cash! {player}: {player.money}"
            assert player.win_points >= 0, f"Negative amount of win points! {player}: {player.win_points}"

    def start_game(self):
        print("""Game is starting! \n""")
        while not self.winner:
            self.data_validation()
            self.start_round()
            self.spy_stage()
            self.spy_income_stage()
            self.construct_stage()
            self.research_stage()
            self.work_stage()
            self.end_round()
            self.round_index = self.round_index + 1
        print(f"{self.winner} has won the game!")
