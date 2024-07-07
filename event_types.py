from enum import Enum


class EventType(Enum):
    """
    Here we can add all the possible events which we are expecting in our backend application. the event
    source can be anything appsflyer,clevertap,manual events from web etc.
    """
    # LOGIN = "login"
    # LOGOUT = "logout"
    # REGISTER = "register"
    PAGE_VISIT = "page_visit"
    ADD_TO_CART = "add_to_cart"
    PURCHASE = "purchase"
    # SEARCH = "search"
    REMOVE_FROM_CART = "remove_from_cart"
