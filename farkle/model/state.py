import random
from itertools import combinations
from collections import OrderedDict

TARGET_SCORE = 1000
POINTS = OrderedDict((
    ('111', 1000),
    ('666', 600),
    ('555', 500),
    ('444', 400),
    ('333', 300),
    ('222', 200),
    ('1', 100),
    ('5', 50),
))


def roll_dice(num):
    return ''.join(sorted(str(random.randint(1, 6)) for _ in range(num)))


def combination(original_list: list[str]):
    """
    Because list_combinations is a list of tuple, so we need to transform the variable to list_result (list of string)
    :param original_list:
    :return: list[str]
    """
    list_combinations = []
    for n in range(1, len(original_list) + 1):
        list_combinations += combinations(original_list, n)
    return list_combinations


class StateDate(object):
    def __init__(self, remaining_dice: str, scoring_dice: list[str]):
        self.remaining_dice = remaining_dice
        self.scoring_dice = scoring_dice

    def __repr__(self):
        return "remaining dice: " + self.remaining_dice + " scoring dice: " + str(self.scoring_dice)

    def number_of_remaining(self):
        return len(self.remaining_dice)

    def number_of_scoring(self):
        return len(self.scoring_dice)


class State(object):
    def __init__(self, state_date: StateDate, score: int, score_total: int, turn_is_over=False, need_to_score=False):
        self.state_date = state_date
        self.score = score
        self.score_total = score_total
        self.need_to_score = need_to_score
        self.turn_is_over = turn_is_over

    def __repr__(self):
        res = str(self.state_date) + " score: " + str(self.score) + " score total: " + str(self.score_total)
        res += " need to score: " + str(self.need_to_score) + " turn_is_over: " + str(self.turn_is_over) + "\n"
        return res

    @property
    def available_combos(self):
        """

        :return: list of string  e.g. ['1', '5']
        """
        if self.need_to_score:
            combos = [combo for combo in POINTS if combo in self.state_date.remaining_dice]
            return [combo for combo in combos]
        else:
            print("You don not need to call in this method!")
            return []

    @property
    def next_states(self):
        """

        :return: list of State
        """
        if self.need_to_score:
            combined_combos = combination(self.available_combos)
            # list of tuple of string  e.g. [('1'), ('5'), ('1', '5')]
            return [self.action_score(combo) for combo in combined_combos]
        else:
            return [self.action_throw(), self.action_bank()]

    @property
    def game_over(self):
        return TARGET_SCORE <= self.score_total

    def action_throw(self):
        if self.state_date.number_of_remaining() == 0:
            new_remaining_dice = roll_dice(6)
            print('Hot dice!')
        else:
            new_remaining_dice = roll_dice(self.state_date.number_of_remaining())

        new_state_date = StateDate(new_remaining_dice, self.state_date.scoring_dice)
        return State(new_state_date, self.score, self.score_total, need_to_score=True)

    def action_score(self, scoring_combos: tuple[str]):
        """

        :param scoring_combos: e.g. ['1', '5'], ['1'] or ['5']
        :return:
        """
        if len(scoring_combos) == 0:
            print('Farkle!')
            new_state_date = StateDate('None', [])
            return State(new_state_date, 0, 0, turn_is_over=True)
        else:
            new_remaining_dice = self.state_date.remaining_dice
            new_scoring_dice = list(scoring_combos)
            new_score = self.score
            for scoring_combo in scoring_combos:
                new_remaining_dice = new_remaining_dice.replace(scoring_combo, '', 1)
                new_score += POINTS[scoring_combo]
            new_state_date = StateDate(new_remaining_dice, new_scoring_dice)
        return State(new_state_date, new_score, self.score_total)

    def action_bank(self):
        new_state_date = StateDate('None', [])
        new_score_total = self.score + self.score_total
        return State(new_state_date, 0, new_score_total, turn_is_over=True)
