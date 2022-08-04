# ID : (AVAILABILITY, NAME, COST, WIN POINTS, (EFFECT1), (EFFECT2))


invention_cards_data = {00: [0, "N", "C", "WP", ("TARGET", "TYPE", "AMOUNT"), ("TARGET", "TYPE", "AMOUNT")],
                        12: [1, "Uzależniająca gra", 0, 1, ("player", "cash", 4)],
                        13: [1, "Cybernetyczne zwierzątko", 0, 1, ("player", "card", 1, "cash", 2)],
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


class Card:
    def __init__(self, card_id: int, name: str, cost: int, win_points: int, effect_1=None, effect_2=None):
        self.id = card_id
        self.name = name
        self.cost = cost
        self.wp = win_points
        self.effect_1 = effect_1
        self.effect_2 = effect_2

    def execute_effects(self, player: object, enemies: list[object]) -> None:
        if self.effect_1:
            pass
        if self.effect_2:
            for enemy in enemies:
                pass
        raise NotImplementedError


def card_parser(card_id: int, data: list) -> Card:
    if len(data) == 4: return Card(card_id, data[1], data[2], data[3])                      # No effects
    if len(data) == 5: return Card(card_id, data[1], data[2], data[3], data[4])             # 1 effect
    if len(data) == 6: return Card(card_id, data[1], data[2], data[3], data[4], data[5])    # 2 effects
    raise ValueError("Wrong card data")
