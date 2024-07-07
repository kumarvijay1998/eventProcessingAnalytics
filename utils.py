from flask import Response
import json
import random
from datetime import datetime, timedelta


def generate_event():
    events = ['page_visit', 'add_to_cart', 'purchase']
    event = random.choice(events)
    customer_id = random.randint(1, 100)
    item_id = random.randint(1, 50)
    timestamp = datetime.now().isoformat()
    event_data = {
        'event': event,
        'customer_id': customer_id,
        'item_id': item_id,
        'timestamp': timestamp
    }
    return event_data


def make_json_response(data,status=200):
    response = Response(
        response=json.dumps(data),
        status=status,
        content_type='application/json'
    )
    return response


def convert_timestamp_util(timestamp):
    return datetime.fromisoformat(timestamp)