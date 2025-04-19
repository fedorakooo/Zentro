from abc import ABC, abstractmethod


class AbstractPickupPointOwnerService(ABC):
    @abstractmethod
    def get_pickup_point_owner_by_id(self):
        pass

    @abstractmethod
    def create_pickup_point_owner(self):
        pass

    @abstractmethod
    def delete_pickup_point_owner(self):
        pass
