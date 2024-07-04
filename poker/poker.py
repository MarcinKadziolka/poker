import poker_func

##############################################################################################################

all_ranges = poker_func.create_ranges()

strong_range = (
    all_ranges[8]
    + all_ranges[9]
    + all_ranges[10]
    + all_ranges[11]
    + all_ranges[12]
    + all_ranges[13]
    + all_ranges[14]
    + all_ranges[16]
    + all_ranges[20]
)


class Game:
    def __init__(self):
        self.table = poker_func.CardHolder()
        self.pot = poker_func.Pot()
        self.deck = poker_func.Deck()

        # variables
        self.small_blind = 10
        self.big_blind = self.small_blind * 2
        self.starting_chip_stack = 1000
        self.num_of_players = 2
        self.folded_count = 0
        self.players = []
        self.preflop = True
        self.flop = False
        self.turn = False
        self.river = False

        self.max_num_of_simulations = 50000
        # To keep count of action in preflop. It has to go at least num_of_players + 2 times, because BB is last to act
        self.iteration = 0

        # Setting button to the last player (his index)
        self.button = self.num_of_players - 1

        # Keeping count of who is to act inside rounds. At first index 0 is first to act (x % x = 0)
        self.index = self.num_of_players
        self.action = self.index % self.num_of_players

    #  Keeping track of the button, after all rounds are finished
    def set_button(self):
        self.button += 1
        self.button = self.button % self.num_of_players

    #  Setting the tracker of action within the round, after moving button
    def set_action(self):
        self.index = self.button + 1 + self.num_of_players
        self.action = self.index % self.num_of_players

    def next_person_turn(self):
        #  If we have 3 players, then the iterating would look like this:
        #  3%3 = 0, 4%3 = 1, 5%3 = 2, 6%3 = 0, ...
        self.index += 1
        self.action = self.index % self.num_of_players

    def reset_game(self):
        self.folded_count = 0
        self.iteration = 0
        self.deck.recollect()
        self.preflop = True
        self.flop = False
        self.turn = False
        self.river = False
        self.table.clear_cards()
        self.pot.highest_bet = 0
        self.pot.chip_stack = 0
        self.pot.last_raise = 0
        for player in self.players:
            player.clear_cards()
            player.current_round_bet = 0
            player.total_bet = 0
            player.folded = False
        input("Round ended, press Enter to continue")

    def create_players(self, type_of_game="Bot"):
        if type_of_game == "Bot":
            self.num_of_players = 2
            self.players.append(poker_func.Player(name="Player"))
            self.players.append(poker_func.Bot())
            for i in range(self.num_of_players):
                self.players[i].chips_inflow(self.starting_chip_stack)
                print(
                    f"Player {self.players[i].get_name()} created, starting chip_stack: {self.players[i].chip_stack}"
                )

        else:
            for i in range(self.num_of_players):
                #  print(f"Enter the name of Player {i}")
                #  name = input()
                self.players.append(poker_func.Player(name=str(i)))
                self.players[i].chips_inflow(self.starting_chip_stack)

                print(
                    f"Player {self.players[i].get_name()} created, starting chip_stack: {self.players[i].chip_stack}"
                )

    def deal_cards(self):
        player = self.players[self.action]
        for _ in range(2):
            for _ in range(self.num_of_players):
                player.draw_card(self.deck.deal())
                print(f"Player {player.get_name()} was dealt a card.")
                self.next_person_turn()
                player = self.players[self.action]

    def pay_small_blind(self):
        player = self.players[self.action]
        flag = player.bet_raise(self.small_blind, self.pot)
        if flag:
            print(
                f"{player.get_name()} pays small blind: {self.small_blind}. chip_stack: {player.get_chip_stack()}"
            )

    def pay_big_blind(self):
        player = self.players[self.action]
        flag = player.bet_raise(self.big_blind, self.pot)
        if flag:
            print(
                f"{player.get_name()} pays big blind: {self.big_blind}. chip_stack: {player.get_chip_stack()}"
            )

    def info_about_players(self, show=0):
        for p in self.players:
            if not p.folded:
                print(f"{p.get_name()}:", end=" ")
                if p.type != "Bot" or show:
                    print(f"{p.get_cards()}. ", end="\n")
                else:
                    print(f"[? ?]. ", end="\n")
                print(
                    f"CRB: {p.get_current_round_bet()}.\n"
                    f"TB: {p.get_total_bet()}.\n"
                    f"B: {p.get_chip_stack()}.",
                    end="\n",
                )
                if p == self.players[self.button]:
                    print(f"BUTTON.")

        print(f"\nPot: {self.pot.get_chip_stack()}")
        print()

    def info_about_player(self):
        player = self.players[self.action]
        to_call = self.pot.get_highest_bet() - player.get_current_round_bet()
        min_raise = to_call + self.pot.get_last_raise()
        name = player.get_name()
        print(
            f"Players {name} turn.\nchip_stack: {player.get_chip_stack()}.\n"
            f"Total bet: {player.get_total_bet()}.\n"
            f"Current round bet: {player.get_current_round_bet()}. "
            f"Pot highest bet: {self.pot.get_highest_bet()}.\nTo call: {to_call}.\n"
            f"Minimum amount to put if you want to raise: {min_raise}\n"
        )

    def get_active_players(self):
        active_players = []
        for player in self.players:
            if not player.folded:
                active_players.append(player)
        return active_players

    def get_active_players_with_positive_chip_stack(self):
        active_players = []
        for player in self.players:
            if not player.folded:
                if player.chip_stack > 0:
                    active_players.append(player)
        return active_players

    # noinspection PyMethodMayBeStatic
    def get_players_hands(self, players):
        hands = []
        for player in players:
            hands.append(player.cards)
        return hands

    #  Presenting player with choices: fold, call, raise, returns True if choice was allowed to make
    def choices(self):
        player = self.players[self.action]
        to_call = self.pot.get_highest_bet() - player.get_current_round_bet()
        min_raise = to_call + self.pot.get_last_raise()
        name = player.get_name()
        decided = False
        print(f"Choose your option {name}:")
        print("1. Fold")
        check = False
        if self.pot.get_highest_bet() == player.get_current_round_bet():
            check = True
            print("2. Check")
        else:
            print(f"2. Call {to_call}")
        if self.preflop:
            print(f"3. Raise (Min amount: {min_raise})")
        else:
            print(f"3. Bet (Min amount: {min_raise})")

        option = int(input("Choice: "))
        if option == 1:
            decided = player.fold()
            if decided:
                self.folded_count += 1
                print(f"Player {name} folded.")
        elif option == 2:
            decided = player.call(self.pot)
            if decided:
                if check:
                    print(
                        f"Player {name} checked. chip_stack: {player.get_chip_stack()}"
                    )
                else:
                    print(
                        f"Player {name}, called, {to_call}. chip_stack: {player.get_chip_stack()}"
                    )
        elif option == 3:
            bet = int(input("Amount: "))
            decided = player.bet_raise(bet, self.pot)
            if decided:
                raised_to = player.get_current_round_bet()
                print(
                    f"Player {name} raised to {raised_to}. chip_stack: {player.get_chip_stack()}"
                )
        else:
            print("Choose between 1 and 3")
        return decided

    def check_folds(self):
        # The player who did not fold is a winner
        if self.folded_count == self.num_of_players - 1:
            return True
        return False

    def check_calls(self):
        # Counting iteration before checking if everyone called, because big blind is last to act
        if self.iteration >= self.num_of_players - 1:
            match_count = 0
            highest_bet = self.pot.get_highest_bet()
            for player in self.players:
                if not player.has_folded():
                    if (
                        player.get_current_round_bet() == highest_bet
                        or player.get_chip_stack() == 0
                    ):
                        match_count += 1
            if match_count == len(self.players) - self.folded_count:
                return True
        self.iteration += 1
        return False

    def check_bankruptcy(self):
        to_delete = []
        for player in self.players:
            if player.get_chip_stack() == 0:
                print(f"{player.get_name()} is bankrupt. He is out of the game!")
                to_delete.append(player)

        self.players = [player for player in self.players if player not in to_delete]

    def check_game_over(self):
        if len(self.players) == 1:
            player = self.players[0]
            print(f"{player.get_name()} is a tournament winner!")
            return True
        return False

    def deal_flop(self):
        for _ in range(3):
            self.table.draw_card(self.deck.deal())

    def next_round(self):
        print("Everyone called")
        # Setting next round
        self.pot.last_raise = 20
        self.pot.highest_bet = 0
        self.iteration = 0
        for p in self.players:
            p.current_round_bet = 0
        self.preflop = False
        self.flop = True
        self.turn = True
        self.river = True

    def showdown(self, players, table, pot):
        final_players = []

        print(f"Table: {table.get_cards()}")
        self.info_about_players(show=1)

        for p in players:
            if not p.has_folded():
                p.cards = p.cards + table.cards
                final_players.append(p)
        sorted_by_score = poker_func.compare_7_card_hands_showdown(final_players)
        #                     0                                        1 / -1
        #  ((Michael, [A♣, 7♢, 9♡, K♠, Q♠], 1414297), (John, [A♣, 7♢, 9♡, K♠, Q♠], 1414297))
        #      0              1               2         0               1               2
        print(sorted_by_score)

        while pot.get_chip_stack() > 0:
            prize = 0
            smallest_total_bet = sorted_by_score[0][0].get_total_bet()
            for p in sorted_by_score:
                if 0 < p[0].get_total_bet() < smallest_total_bet:
                    smallest_total_bet = p[0].get_total_bet()

            print(f"Smallest total bet: {smallest_total_bet}")

            for p in sorted_by_score:
                if p[0].get_total_bet() > 0:
                    p[0].total_bet -= smallest_total_bet
                    prize += smallest_total_bet
                    pot.chip_stack -= smallest_total_bet

            best_score = sorted_by_score[-1][2]

            winners = []
            for t in sorted_by_score:
                if t[2] == best_score:
                    winners.append(t[0])

            odd_chip = prize % len(winners)
            prize = prize // len(winners)
            for w in winners:
                if odd_chip:
                    w.chips_inflow(prize + odd_chip)
                    print(f"{w.get_name()} gets {prize} + {odd_chip} odd chip")
                    odd_chip = 0
                else:
                    w.chips_inflow(prize)
                    print(f"{w.get_name()} gets {prize}")
            sorted_by_score[:] = [
                p for p in sorted_by_score if p[0].get_total_bet() > 0
            ]

    def show_win_probability(self):
        active_players = self.get_active_players()
        active_hands = self.get_players_hands(active_players)

        win_tie_count, amount_of_tables = poker_func.win_probability(
            active_hands,
            self.table.cards,
            self.deck.available_cards,
            self.max_num_of_simulations,
        )

        for i, win_tie in enumerate(win_tie_count):
            print(f"{active_hands[i]},", end=" ")
            print(f"Win: {win_tie[0] / amount_of_tables * 100:.2f} %,", end=" ")
            print(f"Tie: {win_tie[1] / amount_of_tables * 100:.2f} %")

    def preflop_loop(self):

        while True:

            player = self.players[self.action]

            if (
                not player.folded
                and player.current_round_bet <= self.pot.get_highest_bet()
                and player.chip_stack > 0
            ):
                print("########################## PREFLOP ##########################")
                self.info_about_players()

                if player.type == "Bot":
                    to_call = (
                        self.pot.get_highest_bet() - player.get_current_round_bet()
                    )
                    results = poker_func.win_probability_against_range(
                        player.cards, strong_range, self.table.cards, choice="automatic"
                    )
                    pot_odds, break_even = poker_func.pot_odds_break_even(
                        to_call, self.pot.chip_stack
                    )
                    win_prob = results[0] / results[3]

                    self.folded_count = player.decision(
                        win_prob, break_even, self.pot, self.folded_count
                    )

                else:
                    decided = False
                    while not decided:
                        self.info_about_player()
                        decided = self.choices()

                # If check_folds true, finding winner and paying him
                if self.check_folds():
                    for p in self.players:
                        if not p.folded:
                            player = p
                    player.chips_inflow(self.pot.get_chip_stack())
                    print(
                        f"Player {player.get_name()} wins {self.pot.get_chip_stack()}. "
                        f"His chip_stack {player.get_chip_stack()}"
                    )
                    self.reset_game()
                    break

            self.pot.set_highest_bet(self.players)

            if self.check_calls():
                self.next_round()
                break

            print()
            self.next_person_turn()

    def flop_loop(self):
        print()
        print()

        # self.deck.burn_card()
        # print("Burned card")

        self.deal_flop()
        self.set_action()

        while True:

            self.pot.set_highest_bet(self.players)
            player = self.players[self.action]

            if (
                not player.folded
                and player.current_round_bet <= self.pot.get_highest_bet()
                and player.chip_stack > 0
            ):
                print("########################## FLOP ##########################")
                print(f"Table: {self.table.get_cards()}")
                self.info_about_players()

                if player.type == "Bot":
                    to_call = (
                        self.pot.get_highest_bet() - player.get_current_round_bet()
                    )
                    results = poker_func.win_probability_against_range(
                        player.cards, strong_range, self.table.cards, choice="automatic"
                    )
                    pot_odds, break_even = poker_func.pot_odds_break_even(
                        to_call, self.pot.chip_stack
                    )
                    win_prob = results[0] / results[3]

                    self.folded_count = player.decision(
                        win_prob, break_even, self.pot, self.folded_count
                    )

                else:
                    decided = False
                    while not decided:
                        self.info_about_player()
                        decided = self.choices()

                # If check_folds true, finding winner and paying him
                if self.check_folds():
                    for p in self.players:
                        if not p.folded:
                            player = p
                    player.chips_inflow(self.pot.get_chip_stack())
                    print(
                        f"Player {player.get_name()} wins {self.pot.get_chip_stack()}. "
                        f"His chip_stack {player.get_chip_stack()}"
                    )
                    self.reset_game()
                    break

            self.pot.set_highest_bet(self.players)

            if self.check_calls():
                self.next_round()
                break

            print()

            self.next_person_turn()

    def turn_loop(self):
        print()
        # self.deck.burn_card()
        # print("Burned card")
        self.table.draw_card(self.deck.deal())
        self.set_action()

        while True:

            self.pot.set_highest_bet(self.players)

            player = self.players[self.action]

            if (
                not player.folded
                and player.current_round_bet <= self.pot.get_highest_bet()
                and player.chip_stack > 0
            ):
                print("########################## TURN ##########################")
                print(f"Table: {self.table.get_cards()}")
                self.info_about_players()

                if player.type == "Bot":
                    to_call = (
                        self.pot.get_highest_bet() - player.get_current_round_bet()
                    )
                    results = poker_func.win_probability_against_range(
                        player.cards, strong_range, self.table.cards, choice="automatic"
                    )
                    pot_odds, break_even = poker_func.pot_odds_break_even(
                        to_call, self.pot.chip_stack
                    )
                    win_prob = results[0] / results[3]

                    self.folded_count = player.decision(
                        win_prob, break_even, self.pot, self.folded_count
                    )
                else:
                    decided = False
                    while not decided:
                        self.info_about_player()
                        decided = self.choices()

                # If check_folds true, finding winner and paying him
                if self.check_folds():
                    for p in self.players:
                        if not p.folded:
                            player = p
                    player.chips_inflow(self.pot.get_chip_stack())
                    print(
                        f"Player {player.get_name()} wins {self.pot.get_chip_stack()}. "
                        f"His chip_stack {player.get_chip_stack()}"
                    )
                    self.reset_game()
                    break

            self.pot.set_highest_bet(self.players)

            if self.check_calls():
                self.next_round()
                break

            print()

            self.next_person_turn()

    def river_loop(self):
        print()
        # self.deck.burn_card()
        # print("Burned card")
        self.table.draw_card(self.deck.deal())
        self.set_action()

        while True:
            self.pot.set_highest_bet(self.players)
            player = self.players[self.action]

            if (
                not player.folded
                and player.current_round_bet <= self.pot.get_highest_bet()
                and player.chip_stack > 0
            ):
                print("########################## RIVER ##########################")
                print(f"Table: {self.table.get_cards()}")
                self.info_about_players()

                if player.type == "Bot":
                    to_call = (
                        self.pot.get_highest_bet() - player.get_current_round_bet()
                    )
                    results = poker_func.win_probability_against_range(
                        player.cards, strong_range, self.table.cards, choice="automatic"
                    )
                    pot_odds, break_even = poker_func.pot_odds_break_even(
                        to_call, self.pot.chip_stack
                    )
                    win_prob = results[0] / results[3]

                    self.folded_count = player.decision(
                        win_prob, break_even, self.pot, self.folded_count
                    )

                else:
                    decided = False
                    while not decided:
                        self.info_about_player()
                        decided = self.choices()

                # If check_folds true, finding winner and paying him
                if self.check_folds():
                    for p in self.players:
                        if not p.folded:
                            player = p
                    player.chips_inflow(self.pot.get_chip_stack())
                    print(
                        f"Player {player.get_name()} wins {self.pot.get_chip_stack()}. "
                        f"His chip_stack {player.get_chip_stack()}"
                    )
                    self.reset_game()
                    break

            self.pot.set_highest_bet(self.players)

            if self.check_calls():
                print(
                    "**********************************************************************"
                )
                self.showdown(self.players, self.table, self.pot)
                print(
                    "**********************************************************************"
                )
                self.reset_game()
                break

            print()
            self.next_person_turn()

    def run(self):
        # GAME LOOP
        self.create_players(type_of_game="Bot")
        while True:
            self.deck.shuffle()

            self.deal_cards()

            print("########################## BLINDS ##########################")
            # SMALL BLIND AND BIG BLIND
            print()
            self.pay_small_blind()
            self.next_person_turn()
            self.pay_big_blind()
            print()

            self.next_person_turn()

            self.pot.set_highest_bet(self.players)
            if self.preflop:
                self.preflop_loop()
            if self.flop:
                self.flop_loop()
            if self.turn:
                self.turn_loop()
            if self.river:
                self.river_loop()
            print()

            self.check_bankruptcy()
            if self.check_game_over():
                break
            self.num_of_players = len(self.players)
            self.set_button()
            self.set_action()
            self.info_about_players()


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
