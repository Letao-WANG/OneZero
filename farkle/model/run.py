from state import *

state_date = StateDate(roll_dice(6), '')
state = State(state_date, 0, 0, need_to_score=True)
print("state: " + str(state))
print("combos: " + str(state.available_combos))
print("next: " + str(state.next_states))


