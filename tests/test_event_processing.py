import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import patch, mock_open
from datetime import datetime, timedelta
from event_types import EventType
from event_processor import (
    process_event,
    read_and_process_events,
    last_hour_events,
    last_24h_events,
    last_hour_views,
    last_24h_add_to_cart,
    last_24h_sales,
    file_position,
)


class TestEventProcessing(unittest.TestCase):
    def setUp(self):
        # file_position.clear()
        last_hour_events.clear()
        last_24h_events.clear()
        last_hour_views.clear()
        last_24h_add_to_cart.clear()
        last_24h_sales.clear()
        self.test_events = [
            {
                "event": "page_visit",
                "item_id": 1,
                "timestamp": (datetime.now() - timedelta(minutes=30)).strftime(
                    "%Y-%m-%dT%H:%M:%S"
                ),
            },
            {
                "event": "page_visit",
                "item_id": 2,
                "timestamp": (datetime.now() - timedelta(minutes=45)).strftime(
                    "%Y-%m-%dT%H:%M:%S"
                ),
            },
            {
                "event": "add_to_cart",
                "item_id": 1,
                "timestamp": (datetime.now() - timedelta(hours=23)).strftime(
                    "%Y-%m-%dT%H:%M:%S"
                ),
            },
            {
                "event": "purchase",
                "item_id": 1,
                "price": 10.0,
                "timestamp": (
                    datetime.now() - timedelta(hours=23, minutes=59)
                ).strftime("%Y-%m-%dT%H:%M:%S"),
            },
            {
                "event": "page_visit",
                "item_id": 3,
                "timestamp": (
                    datetime.now() - timedelta(hours=28, minutes=59)
                ).strftime("%Y-%m-%dT%H:%M:%S"),
            },
            {
                "event": "add_to_cart",
                "item_id": 3,
                "timestamp": (datetime.now() - timedelta(hours=25)).strftime(
                    "%Y-%m-%dT%H:%M:%S"
                ),
            },
        ]

    def test_page_visit_event(self):
        """
        Tests whether the event is successfully processed or not
        :return:
        """
        event = {
            "event": EventType.PAGE_VISIT.value,
            "item_id": 3,
            "timestamp": (datetime.now()).isoformat(),
        }
        response = process_event(event)
        self.assertEqual(response["data"], "event processed successfully")
        self.assertEqual(last_hour_views[3], 1)

    def test_old_event_removal(self):
        event = {
            "event": EventType.PAGE_VISIT.value,
            "item_id": 4,
            "timestamp": (datetime.now() - timedelta(hours=2)).isoformat(),
        }
        process_event(event)
        self.assertNotIn(4, last_hour_views)

    def test_multiple_event(self):

        for event in self.test_events:
            process_event(event)
        self.assertEqual(last_hour_views[1], 1)
        self.assertEqual(last_hour_views[2], 1)
        self.assertNotIn(
            3, last_hour_views
        )  # Should not include item 3 as it's outside the last hour

        self.assertEqual(last_24h_add_to_cart[1], 1)
        self.assertEqual(last_24h_sales[1], 10.0)
        self.assertNotIn(3, last_24h_add_to_cart)  # Should not include item 3

    def test_missing_key_event(self):
        event = {"event": EventType.PAGE_VISIT.value}
        response = process_event(event)
        self.assertIn("error", response)
        self.assertIn("Missing required key", response["error"])


if __name__ == "__main__":
    unittest.main()
