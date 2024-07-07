import logging
import threading
import time

from flask import Flask, render_template
import json

from event_processor import (
    last_24h_add_to_cart,
    read_and_process_events,
    last_24h_sales,
    last_hour_views,
    last_hour_events,
)
from generate_events import generate_and_append_random_events
from utils import make_json_response

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
app = Flask(__name__)


@app.route("/")
def welcome():
    """
    home page to select the action which you want to perform
    get sales data of last 24 hours etc
    """
    return render_template("welcome.html")



@app.route("/generate_random_events")
def generate_and_append_random_event():
    try:
        generate_and_append_random_events()
        data = {"message": "Random events generated and appended to file"}
        return make_json_response(data)
    except KeyError as e:
        data = {"error": f"required key missing: {str(e)}"}
        return make_json_response(data, status=400)
    except ValueError as e:
        data = {"error": str(e)}
        return make_json_response(data, status=400)
    except IOError as e:
        data = {"error": f"File I/O error: {str(e)}"}
        return make_json_response(data, status=500)
    except Exception as e:
        data = {"error": f"An unexpected error occurred: {str(e)}"}
        return make_json_response(data, status=500)


@app.route("/most_viewed_item",methods=["GET"])
def most_viewed_item():
    try:
        if last_hour_views:
            most_viewed_item_id = max(
                last_hour_views, key=lambda item: last_hour_views[item]
            )
            data = {
                "most_viewed_item": most_viewed_item_id,
                "views": last_hour_views[most_viewed_item_id],
            }
        else:
            data = {"message": "No data available"}
        return make_json_response(data)
    except Exception as e:
        data = {"error": f"An unexpected error occurred: {str(e)}"}
        return make_json_response(data, status=500)  # Internal Server Error for any unexpected error


@app.route("/top_item_added_to_cart", methods=["GET"])
def highest_count_item_added_to_cart():
    try:
        if last_24h_add_to_cart:
            top_item_added_to_card = max(
                last_24h_add_to_cart, key=lambda item: last_24h_add_to_cart[item]
            )
            data= {
                "Most added item id": top_item_added_to_card,
                "number of times added": last_24h_add_to_cart[top_item_added_to_card],
            }
        else:
            data = {"message": "No data available"}
        return make_json_response(data)
    except Exception as e:
        data = {"error": f"An unexpected error occurred: {str(e)}"}
        return make_json_response(data, status=500)  # Internal Server Error for any unexpected error


@app.route("/highest_grossing_item", methods=["GET"])
def highest_grossing_item():
    if last_24h_sales:
        highest_grossing = max(
            last_24h_sales, key=lambda item: last_24h_sales[item]
        )
        data= {
            "highest_grossing_item": highest_grossing,
            "sales": last_24h_sales[highest_grossing],
        }
    else:
        data= {"message": "No data available"}
    return make_json_response(data)


def start_reading_and_processing_events():
    while True:
        read_and_process_events()
        # adding custom sleep timer to sleep for 1 sec before again started reading and processing
        time.sleep(1)


event_processing_thread = threading.Thread(target=start_reading_and_processing_events)
event_processing_thread.daemon = True
event_processing_thread.start()
if __name__ == "__main__":
    app.run(debug=True)
