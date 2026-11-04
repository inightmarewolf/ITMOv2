subscribers = set()


def subscribe(name):
    if not name.strip():
        raise ValueError("empty name")
    subscribers.add(name.strip())
    return {"subscribed": True, "name": name.strip()}


def unsubscribe(name):
    cleaned = name.strip()
    if not cleaned:
        raise ValueError("empty name")
    if cleaned not in subscribers:
        raise ValueError("unknown name")
    subscribers.remove(cleaned)
    return {"unsubscribed": True, "name": cleaned}


def list_subscribers():
    return sorted(subscribers)
