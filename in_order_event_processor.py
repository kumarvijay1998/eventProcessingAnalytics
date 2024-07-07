import json
from collections import deque, defaultdict
from datetime import datetime

from event_types import EventType
from utils import convert_timestamp_util

EVENT_FILE = "events.jsonl"
file_position = 0
# double ended queue to store the events. using dq specifically for removing and adding events from both the sides
recent_events = deque()
daily_events = deque()

# key value store to store the metrics , in real systems we would have used some actual database
last_hour_views = defaultdict(int)
last_24h_add_to_cart = defaultdict(int)
last_24h_sales = defaultdict(float)


def process_event(event):
    try:
        event_type = event["event"]
        item_id = event["item_id"]

        recent_events.append(event)
        daily_events.append(event)
        if event_type == EventType.PAGE_VISIT.value:
            last_hour_views[item_id] += 1
        elif event_type == EventType.ADD_TO_CART.value:
            last_24h_add_to_cart[item_id] += 1
        elif event_type == EventType.PURCHASE.value:
            last_24h_sales[item_id] += event.get("price")
        import pdb
        pdb.set_trace()
        current_time = datetime.now()

        # Removing events which do not lie in the last hour window.
        while (
            recent_events
            and (
                current_time - convert_timestamp_util(recent_events[0]["timestamp"])
            ).total_seconds()
            > 3600
        ):
            old_event = recent_events.popleft()
            if old_event["event"] == EventType.PAGE_VISIT:
                last_hour_views[old_event["item_id"]] -= 1
                if last_hour_views[old_event["item_id"]] == 0:
                    del last_hour_views[old_event["item_id"]]
        # Removing events which do not lie in the last 24 hours window.
        while (
            daily_events
            and (
                current_time - convert_timestamp_util(daily_events[0]["timestamp"])
            ).total_seconds()
            > 86400
        ):
            old_event = daily_events.popleft()
            if old_event["event"] == EventType.ADD_TO_CART:
                last_24h_add_to_cart[old_event["item_id"]] -= 1
                if last_24h_add_to_cart[old_event["item_id"]] == 0:
                    del last_24h_add_to_cart[old_event["item_id"]]
            elif old_event["event"] == EventType.PURCHASE:
                last_24h_sales[old_event["item_id"]] -= old_event.get("price", 0.0)
                if last_24h_sales[old_event["item_id"]] == 0:
                    del last_24h_sales[old_event["item_id"]]
        return {"data": "event processed successfully"}
    except KeyError as e:
        # error handling for missing keys
        return {"error": f"Missing required key: {str(e)}"}

    except ValueError as e:
        # error handling for unknown events
        return {"error": str(e)}

    except Exception as e:
        # other unexpected errors
        return {
            "error": f"An error occurred while processing the event with message {str(e)}"
        }


def read_and_process_events():
    global file_position
    try:
        with open(EVENT_FILE, "r") as file:
            file.seek(file_position)  # Move the file pointer to the last read position
            for event_data in file:
                event = json.loads(event_data)
                process_event(event)

            file_position = file.tell()  # Update the last read value
    except Exception as e:
        print(f"Error reading events: {str(e)}")
