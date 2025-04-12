from enum import Enum


class ProductStatus(Enum):
    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    ARCHIVED = "ARCHIVED"
    REMOVED = "REMOVED"
