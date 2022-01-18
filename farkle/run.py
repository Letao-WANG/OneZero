from player import Player

import random
from collections import OrderedDict

TARGET_SCORE = 4000
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


def input_to_int(message):
    while True:
        try:
            player_num = int(input(message))
        except ValueError:
            print('Incorrect input.')
            continue
        if player_num not in range(0, 100):
            print('Incorrect input.')
            continue
        return player_num


def roll_dice(num):
    return ''.join(sorted(str(random.randint(1, 6)) for _ in range(num)))


def print_status(players):
    """Print total points of players."""
    print('=' * 13, 'Status', '=' * 14)
    for player in players:
        print(player)
    print('=' * 35)


def user_input(combos, chosen):
    while True:
        choice = input('>>> ').lower()
        possible_indices = (str(i + 1) for i in range(len(combos)))
        if choice in possible_indices:
            return choice
        elif chosen and choice in ('r', 'e'):
            return choice


def play_turn(player):
    roll = roll_dice(6)


def play_round(players):
    """:param players: list of Player"""
    for player in players:
        # player['score'] += play_turn(player, players, last_round, max_score)
        if player['score'] >= TARGET_SCORE:
            player['done'] = True
            break
        print('-' * 35)


def main():
    print('=' * 14, 'Farkle', '=' * 14, '\n')
    number_human = 1
    number_ai = 1
    players = [Player(False, name="Human"), Player(True, name="AI")]

    game_over = False
    while not game_over:
        game_over = play_round(players)
        print_status(players)


# play turn
def test(player: Player):
    name = player.name
    total_score = player.score
    roll = roll_dice(6)
    score = 0
    chosen = False
    while True:
        infos = name, score, total_score
        print('{} has score {} and {} banked.'.format(*infos))
        print('Dice:', roll if roll else 'Hot dice!')
        combos = [combo for combo in POINTS if combo in roll]
        if not combos and not chosen:
            print('xxxxxxxxxxxxx FARKLED xxxxxxxxxxxxx')
            score = 0
            break

        for idx, c in enumerate(combos, 1):
            print('({}) Remove {} for {} points.'.format(
                idx, c, POINTS[c]))
        if chosen:
            print('R to roll again.')
            print('E to end your turn.')

        choice = user_input(combos, chosen)
        chosen = True
        if choice == 'e':
            break
        elif choice == 'r':
            chosen = False
            dice_left = len(roll) if roll else 6
            roll = roll_dice(dice_left)
            continue
        combo = combos[int(choice) - 1]
        roll = roll.replace(combo, '', 1)
        score += POINTS[combo]
    return score


if __name__ == '__main__':
    # main()
    test(Player(False, name="Human"))
    input('Thank you for playing.')
