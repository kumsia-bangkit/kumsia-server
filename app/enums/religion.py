from enum import Enum

class Religion(str, Enum):
    ISLAM = "Islam"
    CATHOLICISM = "Catholicism"
    PROTESTANTISM = "Protestantism"
    BUDDHAISM = "Buddhaism"
    HINDUISM = "Hinduism"
    CONFUCIANISM = "Confucianism"
    OTHER = "Other"