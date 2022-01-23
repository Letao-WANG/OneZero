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
    print('Human:')
    while not state.turn_is_over:
        if state.need_to_score:
            print("Dices: " + str(state.dices))
            next_states = state.next_states
            for index, next_state in enumerate(next_states, 1):
                print(str(index) + ') Choose ' + str(next_state.state_data.temp_dice) + ' for scoring ' +
                      str(next_state.state_data.temp_score) + ' points')
            choice = input_int(len(next_states))

            state = next_states[choice-1]
            if len(state.dices) == 6:
                print('Hot dice!')
        else:
            print('1) Choose to continue rolling the remaining dice ')
            print('2) Choose ' + str(state.state_data.scoring_dice) + ' for banking ' +
                  str(state.score) + ' points')
            choice = input_int(2)
            state = state.next_states[choice-1]
            if len(state.available_dices) == 0:
                print('Farkle!')
    print(state)
    return state


def ai_play_turn(state: State):
    print('AI:')
    while not state.turn_is_over:
        next_states = state.next_states
        state = random.choice(next_states)
        print(str(state))
    return state


def play_round(state: State, ai_state: State):
    while not state.turn_is_over:
        state = human_play_turn(state)
    while not ai_state.turn_is_over:
        ai_state = ai_play_turn(ai_state)
    return state, ai_state


def play_game(state: State, ai_state: State):
    while not state.game_over and not ai_state.game_over:
        state, ai_state = play_round(state, ai_state)
        print('state: ' + str(state))
        print('ai:' + str(ai_state))
        state.turn_is_over = False
        ai_state.turn_is_over = False
    print("Game over!")
    print('state: ' + str(state))
    print('ai:' + str(ai_state))


def main():
    print('Welcome to the farkle game!')
    original_state = State(StateData('', []))
    original_state = original_state.action_throw()
    ai_state = State(StateData(roll_dice(6), []), need_to_score=True)
    play_game(original_state, ai_state)


main()
