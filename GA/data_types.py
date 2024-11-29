
from enum import Enum
from typing import List


class NextGenSelectionType(Enum):
    RBS = "RBS" # ranking based selection
    FPS = "FPS" # improved fitness proportionate selection
    TRS = "TRS" # tournament selection


# for selection types from new population
class SelectionType(Enum):
    GENERAL_REPLACEMENT = "GENERAL_REPLACEMENT"
    ELITISM = "ELITISM"
    GRADUAL_REPLACEMENT = "GRADUAL_REPLACEMENT"


# enums for ranking based selection types
class RBSType(Enum):
    LINEAR_RANKING = "LINEAR_RANKING"
    EXPONENTIAL_RANKING = "EXPONENTIAL_RANKING"


# enum that has 2 possible values: windoing, signa_scaling for probability calculation
class FPSType(Enum):
    WINDOWING = "WINDOWING"
    SIGNAL_SCALING = "SIGNAL_SCALING"


# enum for probability based selection
class ProbabilityBasedSampleMethodType(Enum):
    ROULETTE_WHEEL = "ROULETTE_WHEEL"
    STOCHASTIC_UNIVERSAL_SAMPLING = "STOCHASTIC_UNIVERSAL_SAMPLING"


# enum for crossover types
class CrossOverType(Enum):
    SINGLE_POINT = "SINGLE_POINT"
    TWO_POINT = "TWO_POINT"
    UNIFORM = "UNIFORM"
