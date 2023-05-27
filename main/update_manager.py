events = dict()

def need_user(func):
    def wrapper(user, *args, **kwargs):
        if user.id not in events:
            events[user.id] = []
        func(user=user, *args, **kwargs)
    return wrapper

def flush(user):
    events[user.id] = []
    
def delete(user):
    events.pop(user.id)

@need_user
def push_event(user, event):
    events[user.id].append(event)

@need_user
def request_update(user):
    update = events[user.id].copy()
    events[user.id] = []
    
    return update
