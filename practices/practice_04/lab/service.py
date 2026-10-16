subscribers = set()


def subscribe(name):
    if not name.strip():
        raise ValueError("empty name")
    subscribers.add(name.strip())
    return {"subscribed": True, "name": name.strip()}


def list_subscribers():
    return sorted(subscribers)

# hook-demo
