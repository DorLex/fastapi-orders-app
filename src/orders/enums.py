from enum import Enum


class OrderStatusEnum(Enum):
    created = 'created'
    in_processing = 'in_processing'
    completed = 'completed'
    canceled = 'canceled'
