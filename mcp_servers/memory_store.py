_store = {}

def save_turn(session_id: str, question: str, answer: str):
    if session_id not in _store:
        _store[session_id] = []
    _store[session_id].append({
        "question": question,
        "answer": answer
    })

def get_history(session_id: str):
    return _store.get(session_id, [])

class MemoryStore:
    def save_turn(self, session_id, question, answer):
        save_turn(session_id, question, answer)

    def get_history(self, session_id):
        return get_history(session_id)

memory_store = MemoryStore()
