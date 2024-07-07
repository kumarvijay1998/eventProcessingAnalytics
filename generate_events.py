import json
import random
import uuid
from datetime import datetime
from event_types import EventType

EVENT_FILE = "events.jsonl"


class EventGenerationUtils:
    @classmethod
    def get_timestamp(cls):
        now = datetime.now()
        return now.isoformat()

    @classmethod
    def get_customer_id(cls):
        return random.randint(1, 1000)

    @classmethod
    def get_item_id(cls):
        return random.randint(1, 1000)

    @classmethod
    def get_price(cls):
        return random.randint(10, 500)


def generate_event(event_type):
    item_id = EventGenerationUtils.get_item_id()
    base_event = {
        "event": event_type.value,
        "timestamp": EventGenerationUtils.get_timestamp(),
        "customer_id": EventGenerationUtils.get_customer_id(),
        "item_id": item_id
    }

    if event_type in [
        EventType.ADD_TO_CART,
        EventType.PURCHASE,
        EventType.REMOVE_FROM_CART,
    ]:
        base_event.update(
            {
                "item_id": item_id,
                "quantity": random.randint(1, 5),
                "price": EventGenerationUtils.get_price(),
            }
        )
        if event_type == EventType.PURCHASE:
            base_event["total_amount"] = base_event["quantity"] * base_event["price"]

    elif event_type == EventType.PAGE_VISIT:
        base_event[
            "page_url"
        ] = f"https://borneo.io/product/{item_id}"

    # elif event_type == EventType.REGISTER:
    #     base_event["email"] = f"{uuid.uuid4()}@gmail.com"
    #     base_event["name"] = f"Customer {random.randint(1, 1000)}"
    #
    # elif event_type == EventType.SEARCH:
    #     base_event["search_query"] = random.choice(
    #         ["earphones", "mobile", "headphones", "marker", "table"]
    #     )

    return base_event


def append_event_to_file(event):
    """
    write events to EventFile
    """
    with open(EVENT_FILE, "a") as file:
        file.write(json.dumps(event) + "\n")


def generate_and_append_random_events():
    """
    randomly generates events and append to events file
    Simulating the real producer behavior.
    """
    event_types = list(EventType)
    # randomly generate 100 events
    for _ in range(100):
        event_type = random.choice(event_types)
        event = generate_event(event_type)
        append_event_to_file(event)