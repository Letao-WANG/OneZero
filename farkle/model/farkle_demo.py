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


def play_turn(state: State):
    print('Human:')
    while True:
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
            print(state)
        else:
            print('1) Choose to continue rolling the remaining dice ')
            print('2) Choose ' + str(state.state_data.scoring_dice) + ' for banking ' +
                  str(state.score) + ' points')
            choice = input_int(2)
            state = state.next_states[choice-1]
            if choice == 2:
                return state
            if len(state.available_dices) == 0:
                print('Farkle!')
                return state
            print(state)


def ai_play_turn(state: State):
    print('AI:')
    next_states = state.next_states
    return next_states[random.randint(0, len(next_states))]


def play_round(state: State, ai_state: State):
    while not state.game_over or not ai_state.game_over:
        state = play_turn(state)
        ai_state = ai_play_turn(ai_state)
    print("Game over!")
    print('state: ' + str(state))
    print('ai:' + str(ai_state))


def main():
    print('Welcome to the farkle game!')
    original_state = State(StateData(roll_dice(6), []), 0, 0, need_to_score=True)
    ai_state = State(StateData(roll_dice(6), []), 0, 0, need_to_score=True)
    play_round(original_state, ai_state)


main()
