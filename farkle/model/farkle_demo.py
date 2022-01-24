from state import *


def input_int(max_number: int):
    while True:
        try:
            number = int(input('>>> '))
        except ValueError:
            print('Incorrect input.')
            continue
        if number not in range(1, max_number + 1):
            print('Incorrect input.')
            continue
        return number


def human_play_turn(state: State):
    print(20 * '-' + ' Human turn begins: ' + 20 * '-')
    while not state.turn_is_over:
        if state.need_to_score:
            print("Dices to throw: " + str(state.state_dice.remaining_dice))
            next_states = state.next_states
            for index, next_state in enumerate(next_states, 1):
                print(str(index) + ') Choose ' + str(next_state.state_dice.temp_dice) + ' for scoring ' +
                      str(next_state.state_dice.temp_score) + ' points')
            choice = input_int(len(next_states))

            state = next_states[choice - 1]
            if len(state.state_dice.remaining_dice) == 6:
                print('Hot dice!')
        else:
            print('1) Choose to continue rolling the remaining dice ')
            print('2) Choose ' + str(state.state_dice.scoring_dice) + ' for banking ' +
                  str(state.score) + ' points')
            choice = input_int(2)
            state = state.next_states[choice - 1]
            if len(state.available_dices) == 0:
                print('Farkle!')
    print('Human total score:' + str(state.score_total))
    return state


def ai_strategy(next_states):
    state = random.choice(next_states)
    return state


def ai_play_turn(state: State):
    print(20 * '-' + ' AI turn begins: ' + 20 * '-')
    while not state.turn_is_over:
        next_states = state.next_states
        state = ai_strategy(next_states)
        print(str(state))
    return state


def play_round(state: State, ai_state: State):
    while not state.turn_is_over:
        state = human_play_turn(state)
    while not ai_state.turn_is_over:
        ai_state = ai_play_turn(ai_state)
    return state, ai_state


def play_game(state: State, ai_state: State):
    num_round = 1
    while not state.game_over and not ai_state.game_over:
        print('\n' + 'Round ' + str(num_round) + ' begins: ')
        state, ai_state = play_round(state, ai_state)
        num_round += 1
        print(20 * '-' + ' Round over! ' + 20 * '-')
        print('Human total score:' + str(state.score_total))
        print('AI total score:' + str(ai_state.score_total))
        state.turn_is_over = False
        ai_state.turn_is_over = False
    print('\n' + 20 * '*' + ' Game over! ' + 20 * '*')
    result = 'Human' if state.score_total > ai_state.score_total else 'AI'
    print('Winner is ' + result + '!')


def main():
    print('Welcome to the farkle game!')
    original_state = State(StateDice('', [])).action_throw()
    ai_state = State(StateDice(roll_dice(6), []), need_to_score=True)
    play_game(original_state, ai_state)


main()
