from models.product import Product

class CompetitorResearchAgent:
    def __init__(self, platform: str):
        self.platform = platform

    def fetch_competitors(self, product: Product):
        if self.platform == "etsy":
            from agents.competitor_search.etsy_competitors import EtsyCompetitorResearchAgent
            return EtsyCompetitorResearchAgent().fetch_competitors(product)
        # elif self.platform == "amazon": ...
        # elif self.platform == "shopify": ...
        else:
            return {"error": f"Unsupported platform {self.platform}"}