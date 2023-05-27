events = dict()

def need_user(func):
    def wrapper(user, *args, **kwargs):
        if user not in events:
            events[user] = []
        func(user=user, *args, **kwargs)
    return wrapper

def flush(user):
    events[user] = []
    
def delete(user):
    events.pop(user)

@need_user
def push_event(user, event):
    events[user].append(event)

@need_user
def request_update(user):
    update = events[user].copy()
    events[user] = []
    
    return update
