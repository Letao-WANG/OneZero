from state import *

state_date = StateDate('111333', '')
state = State(state_date, 0, 0, need_to_score=True)
print(state)
print("state actions: " + str(combination(state.available_combos)))
# print(str(state.next_states))


