from pupdb.core import PupDB
from database.model import State

db = PupDB('F:/python/radiator_panel/andrey_bot/database/db.json')

def get_state(user_id) -> State:
    state_data = db.get(user_id)
    if state_data is None:
        state = State(user_id)
        save_state(state)
        return state
    return State(user_id, state_data)

def save_state(state: State):
    db.set(state.user_id, state.data)

