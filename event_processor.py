from sortedcontainers import SortedDict
import json
from collections import defaultdict
from datetime import datetime, timedelta
from event_types import EventType
from utils import convert_timestamp_util

EVENT_FILE = "events.jsonl"
file_position = 0

"""
Sorted dictionary to store events by timestamp so that we don't have to iterate through the complete queue
there is possibility that out of order events can come from file so to efficiently removing it we are using
this sorted dict.
"""
last_hour_events = SortedDict()  # to store the last hour events
last_24h_events = SortedDict()  # to store the last 24h events

# In memory Key-value store to store the metrics
last_hour_views = defaultdict(int)
last_24h_add_to_cart = defaultdict(int)
last_24h_sales = defaultdict(float)


def process_event(event):
    try:
        event_type = event["event"]
        item_id = event["item_id"]
        event_timestamp = convert_timestamp_util(event["timestamp"])

        last_hour_events[event_timestamp] = event
        last_24h_events[event_timestamp] = event

        if event_type == EventType.PAGE_VISIT.value:
            last_hour_views[item_id] += 1
        elif event_type == EventType.ADD_TO_CART.value:
            last_24h_add_to_cart[item_id] += 1
        elif event_type == EventType.PURCHASE.value:
            last_24h_sales[item_id] += event.get("price", 0.0)

        current_time = datetime.now()

        # Remove events which do not lie in the last hour window.
        cut_off_time = current_time - timedelta(hours=1)
        for timestamp in list(last_hour_events.keys()):
            if timestamp > cut_off_time:
                break
            old_event = last_hour_events.pop(timestamp)
            if old_event["event"] == EventType.PAGE_VISIT.value:
                last_hour_views[old_event["item_id"]] -= 1
                if last_hour_views[old_event["item_id"]] == 0:
                    del last_hour_views[old_event["item_id"]]

        # Remove events which do not lie in the last 24 hours window.
        cut_off_time = current_time - timedelta(days=1)
        for timestamp in list(last_24h_events.keys()):
            if timestamp > cut_off_time:
                break
            old_event = last_24h_events.pop(timestamp)
            if old_event["event"] == EventType.ADD_TO_CART.value:
                last_24h_add_to_cart[old_event["item_id"]] -= 1
                if last_24h_add_to_cart[old_event["item_id"]] == 0:
                    del last_24h_add_to_cart[old_event["item_id"]]
            elif old_event["event"] == EventType.PURCHASE.value:
                last_24h_sales[old_event["item_id"]] -= old_event.get("price", 0.0)
                if last_24h_sales[old_event["item_id"]] == 0:
                    del last_24h_sales[old_event["item_id"]]

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
