# from models.product import Product
# from agents.competitor_search.etsy_competitors import EtsyCompetitorResearchAgent

# Instantiate the agent
# agent = EtsyCompetitorResearchAgent()

# Create a test product
# prod = Product(title="Handmade Ceramic Mug", description="A small clay mug")

# Fetch competitors
# result = agent.fetch_competitors(prod)

# Print the output to see what the scraper returned
# print("SCRAPER RESULT:", result)

from models.product import Product
from agents.etsy import EtsyAgent

# Example product to optimize
prod = Product(
    title="Handmade Ceramic Mug",
    description="A rustic, hand-thrown ceramic mug perfect for coffee or tea lovers.",
    price=28.00
)

agent = EtsyAgent()
optimized_listing = agent.optimize(prod)  # no competitors passed → loads synthetic_competitors.json
print("OPTIMIZED LISTING:", optimized_listing)