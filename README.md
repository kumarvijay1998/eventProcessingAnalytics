# Event Processing Analytics with Flask

This project demonstrates real-time event processing and analytics using Flask. It analyzes events such as page visits, add-to-cart actions, and purchases to generate insights.

## Setup

### Prerequisites

- Python (3.6 or higher)
- Git

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/kumarvijay1998/eventProcessingAnalytics.git
   cd eventProcessingAnalytics
2. Set up a virtual environment (optional but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. Install dependencies:
   ```bash
   pip3 install -r requirements.txt
   
### Running and Testing application
1. Test cases running:
   ```bash
   pytest
2. Running the Application:
   ```bash
   python3 app.py
   

### Accessing application
you will get the local url on which the application is running, click on that and it will open the browser.

### API Endpoints

#### 1. Generate Random Events
- **Endpoint:** `/generate_random_events`
- **Method:** `GET`
- **Description:** Generates a random event and appends it to the `events.jsonl` file.
- **Request:**
  ```bash
  curl http://127.0.0.1:5000/generate_random_events
- **Response:**
  ```bash
  {"message": "Random event generated and appended to file"}


   
#### 2. Most Viewed Item
- **Endpoint:** `/most_viewed_item`
- **Method:** `GET`
- **Description:** Returns the most viewed item in the last hour.
- **Request:**
  ```bash
  curl http://127.0.0.1:5000/most_viewed_item
- **Response:**
  ```bash
  {"most_viewed_item": 1, "views": 10}
  
#### 3. Top Item Added to Cart
- **Endpoint:** `/top_item_added_to_cart`
- **Method:** `GET`
- **Description:** Returns the item most added to cart in the last 24 hours.
- **Request:**
  ```bash
  curl http://127.0.0.1:5000/top_item_added_to_cart
- **Response:**
  ```bash
  {"top_item_added_to_cart": 2,"adds_to_cart": 5}
  
#### 4. Highest Grossing Item
- **Endpoint:** `/highest_grossing_item`
- **Method:** `GET`
- **Description:** Returns the highest-grossing item (total sales) in the last 24 hours.
- **Request:**
  ```bash
  curl http://127.0.0.1:5000/highest_grossing_item
- **Response:**
  ```bash
  {"highest_grossing_item": 3, "total_sales": 1300.00}
  

### Event Processing Logic and explanation
1. **Random Event Generation:**
    - we are randomly generating events with the help of `generate_and_append_random_events()`. in this we are
    generating some random 100 events like page_visit,add_to_cart etc and appending to the file(simulating
      the producer behavior in real scenarios )
   - we are also running one separate thread to consume this event (simulating the consumer behaviour in real)
     the function which is performing this work is read_and_process_events()
   - The `read_and_process_events` function reads new events from the `events.jsonl` file and processes them using the `process_event` function.

    
2. **Process event logic:**
   - Processed events are stored in two sorted dict (sorted based on timestamp):
     - `recent_events`: Stores events from the last hour.
     - `daily_events`: Stores events from the last 24 hours.
   - Metrics are updated based on the event type:
     - `last_hour_views` Tracks the number of views for each item in the last hour.
     - `last_24h_add_to_cart` Tracks the number of times items were added to cart in the last 24 hours.
     - `last_24h_sales` Tracks the total sales for each item in the last 24 hours. 
       
3. **Alternate approach:**
    - initially we were using deque so that removing directly from the front but later we thought
    that there is possibility of older events in the middle of the queue, so then we used SortedDict to store
      the events based on the timestamps so that our logic to remove is accurate, and we don't need to iterate
      to all the elements of the queue
      - But we have not removed our old logic which was using deque and was assuming that events will be in-
    order so that code is present in `in_order_event_processor.py` file but currently is not in use.
4. **Assumptions:** 
   - The events can be out of order as well
   - Each event is assumed to have the necessary attributes (`event`, `timestamp`, `item_id`, `customer_id`, `price`)
    
5. **Demo Video:**
    [Demo Video](https://drive.google.com/file/d/1WmSnTF_N6ZPXMo3jAZTi8Kl1LO1ebXTT/view?usp=share_link)

