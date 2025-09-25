# pip install fastapi uvicorn openai python-multipart

from fastapi import FastAPI, UploadFile, Form
from pydantic import BaseModel
from typing import Optional
from models.product import Product
from agents.competitor_search.base import CompetitorResearchAgent
from agents.etsy import EtsyAgent
# from agents.ebay import EbayAgent
# from agents.shopify import ShopifyAgent
from dotenv import load_dotenv
import os

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# Define schema for JSON input (when user types product info in a textbox)
class ProductInput(BaseModel):
    title: Optional[str] = None
    description: str
    price: Optional[float] = None

@app.get("/")
def root():
    return {"message": "Octolist backend is running 🚀"}

# 1) JSON/text input route
@app.post("/ingest/json")
def ingest_json(product: ProductInput):
    """
    Handles JSON input for product description
    """
    # For now just echo back
    return {
        "canonical_schema": {
            "title": product.title or "Untitled Product",
            "description": product.description,
            "price": product.price or "N/A",
        }
    }

# 2) Image upload route
@app.post("/ingest/image")
async def ingest_image(file: UploadFile):
    """
    Handles image upload for product
    """
    # For now just return filename
    return {"filename": file.filename}

# Optimize listings
competitor_agent = CompetitorResearchAgent(platform="etsy")
etsy_agent = EtsyAgent()
# ebay_agent = EbayAgent()
# shopify_agent = ShopifyAgent()

@app.post("/optimize")
def optimize_product(product: Product):
    # 1) Competitor insights
    competitors = competitor_agent.fetch_competitors(product)
    # 2) Optimized listing generation
    etsy_listing = etsy_agent.optimize(product, competitors)

    return {"optimized_listings": [etsy_listing.dict()]}