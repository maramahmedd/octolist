from abc import ABC, abstractmethod
from models.product import Product

class BaseAgent(ABC):
    @abstractmethod
    def optimize(self, product: Product) -> dict:
        """Takes a Product and returns an optimized listing dict"""
        pass