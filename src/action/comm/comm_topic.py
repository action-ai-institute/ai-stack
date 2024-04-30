from enum import Enum


class CommTopic(str, Enum):
    POTENTIAL_ATTACK = "potential_attack"
    LOG = "log"
