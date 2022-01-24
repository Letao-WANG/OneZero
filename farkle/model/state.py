import random
from itertools import combinations
from collections import OrderedDict

TARGET_SCORE = 1000
POINTS = OrderedDict((
    ('123456', 1500),
    ('12345', 500),
    ('23456', 700),
    ('11111', 4000),
    ('66666', 2400),
    ('55555', 2000),
    ('44444', 1600),
    ('33333', 1200),
    ('22222', 800),
    ('1111', 2000),
    ('6666', 1200),
    ('5555', 1000),
    ('4444', 800),
    ('3333', 600),
    ('2222', 400),
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
    """
    Simulate dice roll
    :param num: number of dice
    :return: collection of dice represented by string, e.g. '123456'
    """
    return ''.join(sorted(str(random.randint(1, 6)) for _ in range(num)))


class StateDice(object):
    """
    This class stores information of dice state.

    The difference between scoring_dice and temp_dice is that scoring_dice can be stored in the next state data,
    but not for temp_dice. Basically using in the interaction of the user.

    Attributes:
        remaining_dice: dices that still can be thrown
        scoring_dice: type list[str], dices that have been selected and scored
        temp_dice: dices that have been selected only in the current state
        temp_score: score according to the sum of temp_dice
    """

    def __init__(self, remaining_dice: str, scoring_dice: list[str], temp_dice=None, temp_score=None):
        self.remaining_dice = remaining_dice
        self.scoring_dice = scoring_dice
        self.temp_dice = temp_dice
        self.temp_score = temp_score

    def __repr__(self):
        return "remaining dice: " + self.remaining_dice + ", scoring dice: " + str(self.scoring_dice)

    def number_of_remaining(self):
        return len(self.remaining_dice)

    def number_of_scoring(self):
        return len(self.scoring_dice)


def verify_combo(t: tuple[str]):
    """
    Make sure that the combo of tuple are not duplicated
    :param t: e.g. ('1', '5', '15') or ('12345', '1', '5') or ('111', '1')
    :return:
    """
    for i in range(0, len(t)):
        for j in range(i + 1, len(t)):
            if t[i] in t[j] or t[j] in t[i]:
                return False
    return True


def combination(original_list: list[str]):
    """
    Combination of list, using for find possible combos.

    Because list_combinations is a list of tuple, so we need to transform the variable to list_result
    (list of string)
    :param original_list:       e.g. ['1', '5']
    :return: list[tuple(str)]   e.g. ['1', '5', '15']
    """
    list_combinations = []
    for n in range(1, len(original_list) + 1):
        combos = combinations(original_list, n)
        for combo in combos:
            if verify_combo(combo):
                list_combinations.append(combo)
    return list_combinations


class State(object):
    """
    Basic class of game information.

    One state corresponds to one player, it includes all the information of a game moment.
    When the game advances, an instance of State develop to the next State,
    and there are 3 actions (throw, score, bank) to realize it.

    How to use:
    self.next_states: to get the list of possible next state
    (could be developed by action throw, score or bank, it depends on the variable need_to_score)
    self.action_throw: to get the next state after executing the action throw. Score, bank too.

    Attributes:
        state_dice: information of dice state
        score: score obtained in this turn
        score_total: total score that has been banked
        need_to_score: if it is necessary to score a combo in the current state
        turn_is_over: if this turn has overed
    """

    def __init__(self, state_dice: StateDice, score=0, score_total=0, turn_is_over=False, need_to_score=False):
        self.state_dice = state_dice
        self.score = score
        self.score_total = score_total
        self.need_to_score = need_to_score
        self.turn_is_over = turn_is_over

    def __repr__(self):
        res = str(self.state_dice) + ", score: " + str(self.score) + ", score total: " + str(self.score_total)
        res += ", need to score: " + str(self.need_to_score) + ", turn_is_over: " + str(self.turn_is_over)
        return res

    @property
    def dices(self):
        """
        remaining dices, for simplicity
        :return: remaining_dice
        """
        return self.state_dice.remaining_dice

    @property
    def available_dices(self):
        """
        Get all the possible combo dices with combination
        :return: e.g. ['1', '5', '15']
        """
        return combination(self.available_combos)

    @property
    def available_combos(self):
        """
        Get all the possible combo dices without combination
        :return: list of string  e.g. ['1', '5']
        """
        if self.need_to_score:
            combos = [combo for combo in POINTS if combo in self.state_dice.remaining_dice]
            return [combo for combo in combos]
        else:
            return []

    @property
    def next_states(self):
        """
        Develop to the next state of game
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
        """
        Action to throw the dices
        :return: next state after throwing
        """
        if self.state_dice.number_of_remaining() == 0:
            new_remaining_dice = roll_dice(6)
        else:
            new_remaining_dice = roll_dice(self.state_dice.number_of_remaining())
        new_state_data = StateDice(new_remaining_dice, self.state_dice.scoring_dice)
        new_state = State(new_state_data, self.score, self.score_total, need_to_score=True)

        if len(new_state.available_combos) == 0 and len(new_state.state_dice.remaining_dice) != 0:
            # Farkle !
            return State(new_state_data, score=0, score_total=self.score_total, turn_is_over=True)
        else:
            return new_state

    def action_score(self, scoring_combos: tuple[str]):
        """
        Action to score selected dices.
        Move the selected dices (scoring_combos) from remaining_dice to scoring_dice.

        :param scoring_combos: e.g. ['1', '5'], ['1'] or ['5']
        :return: next state after scoring
        """
        new_remaining_dice = self.state_dice.remaining_dice
        new_scoring_dice = self.state_dice.scoring_dice + list(scoring_combos)
        new_score = self.score

        temp_score = 0
        for scoring_combo in scoring_combos:
            new_remaining_dice = new_remaining_dice.replace(scoring_combo, '', 1)
            new_score += POINTS[scoring_combo]
            temp_score += POINTS[scoring_combo]

        new_state_data = StateDice(new_remaining_dice, new_scoring_dice, scoring_combos, temp_score)
        new_state = State(new_state_data, new_score, self.score_total)

        if len(new_state.state_dice.remaining_dice) == 0:
            # Hot dice!
            return State(StateDice(roll_dice(6), [], scoring_combos, temp_score), new_state.score, self.score_total,
                         need_to_score=True)
        else:
            return new_state

    def action_bank(self):
        """
        Action to bank the score
        :return: end state with total score
        """
        new_score_total = self.score + self.score_total
        return State(StateDice(roll_dice(6), []), score_total=new_score_total, need_to_score=True, turn_is_over=True)
