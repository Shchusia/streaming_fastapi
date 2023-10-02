from enum import Enum


class WebrtcRoutes(str, Enum):
    GET_OFFER_SERVER = '/get_offer'
    POST_RECEIVE_ANSWER = '/publisher_answer'
