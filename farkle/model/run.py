from state import *

# state_date = StateDate('23456', ['1'])
state_date = StateDate('123456', [])
state = State(state_date, 0, 0, need_to_score=True)

# print(state)
# print(state.action_score(('5', )))

next_states = state.next_states
print(next_states)
