from enum import Enum

class Gender(str, Enum):
    Female = "Female"
    Male = "Male"

class Religion(str, Enum):
    Hindu = "Hindu"
    Islam = "Islam"
    Kristen = "Kristen"
    Buddha = "Buddha"
    Katolik = "Katolik"
    Konghucu = "Konghucu"