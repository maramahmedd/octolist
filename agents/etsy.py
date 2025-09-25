from openai import OpenAI
from models.product import Product
from models.listing import Listing
from .base import BaseAgent
from dotenv import load_dotenv
import os
import json

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

class EtsyAgent(BaseAgent):
    def optimize(self, product: Product, competitors: dict = None) -> Listing:
        # -------------------------------
        # DEMO MODE: load synthetic competitors
        # Comment this block out later when using real scraper/API
        if competitors is None:
            with open("data/synthetic_competitors_etsy.json", "r", encoding="utf-8") as f:
                competitors = json.load(f)
        # -------------------------------
                
        # Build competitor summary
        if "competitors" not in competitors:
            raise ValueError(f"No competitor data returned: {competitors}")

        comp_titles = [c["title"] for c in competitors["competitors"]]
        avg_price = competitors["avg_price"]

        # Prompt engineering
        system_prompt = """
        You are an expert Etsy listing optimizer.
        Your job is to create product listings that maximize visibility and conversions.
        Etsy listings should be:
        - Storytelling-driven and personal (customers love handmade uniqueness).
        - Keyword-rich but natural (so they rank in Etsy search).
        - Under Etsy's character limits (Title: 140 chars, Tags: 13 tags).
        - Include clear benefits and emotional appeal.
        - Optimized price suggestion based on competitor analysis.
        Return your answer as valid JSON matching this schema:
        {
          "platform": "etsy",
          "title": "...",
          "description": "...",
          "tags": ["..."],
          "suggested_price": 0.00
        }
        """
        
        # NEW: feed competitor details, not just titles
        competitor_summary = "\n".join(
            [f"- {c['title']} (${c['price']}), tags: {', '.join(c['tags'])}" 
             for c in competitors["competitors"][:5]]
        )

        user_prompt = f"""
        Product Info:
        Title: {product.title}
        Description: {product.description}
        Price (if provided): {product.price}

        Competitors:
        Avg Price: {avg_price}
        Top Competitors:
        {competitor_summary}

        Please return a fully optimized Etsy listing.
        """

        response = client.chat.completions.create(
            model="gpt-5",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={ "type": "json_object" }
        )

        output = response.choices[0].message.content

        # Parse JSON safely
        try:
            output_json = json.loads(output)
        except json.JSONDecodeError as e:
            raise ValueError(f"LLM did not return valid JSON: {e}\n\n{output}")

        # Convert JSON dict → Pydantic model
        return Listing(**output_json)