from enum import Enum


class UserRole(Enum):
    SELLER = "Seller"
    BUYER = "Buyer"
    DELIVERY_OWNER = "DeliveryOwner"
    ACTIVITY_CONFIRMER = "ActivityConfirmer"
    ADMIN = "Admin"
