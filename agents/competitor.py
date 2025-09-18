import requests
from models.product import Product

class CompetitorResearchAgent:
    def fetch_competitors(self, product: Product) -> dict:
        # Later: call Etsy API. For now: fake search w/ Etsy public search
        query = product.title.replace(" ", "+")
        url = f"https://www.etsy.com/search?q={query}"

        # TODOs: scrape results properly w/ BeautifulSoup (HTML parsing)
        # For now: return mock data
        competitors = [
            {"title": f"Handmade {product.title}", "price": 19.99, "tags": ["handmade", "gift"]},
            {"title": f"{product.title} - Trending", "price": 24.99, "tags": ["popular", "sale"]},
        ]

        avg_price = sum(c["price"] for c in competitors) / len(competitors)

        return {
            "platform": "etsy",
            "competitors": competitors,
            "avg_price": avg_price
        }
