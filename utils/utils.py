import random

def trigger_random_event(game_state):
    events = [
        {"name": "Economic Boom", "gdp": 10, "public_approval": 5},
        {"name": "Recession", "gdp": -10, "public_approval": -5},
        {"name": "Scientific Breakthrough", "public_approval": 10},
        {"name": "Corruption Scandal", "public_approval": -10},
        {"name": "Natural Disaster", "budget": -50, "public_approval": -5},
    ]

    if "event_history" not in game_state:
        game_state["event_history"] = []

    if random.random() < 0.3:  # 30% chance of an event happening
        event = random.choice(events)
        for key, value in event.items():
            if key != "name":
                game_state[key] += value

        game_state["event_history"].append(event["name"])
        return event["name"]
    return None

