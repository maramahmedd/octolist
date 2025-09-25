# scripts/generate_synthetic_competitors.py
import json
import random

base_titles = [
    "Handmade Ceramic Mug",
    "Speckled Coffee Cup",
    "Rustic Clay Mug",
    "Stoneware Tea Mug",
    "Glazed Pottery Mug"
]
adjectives = ["Cozy", "Minimalist", "Vintage", "Hand-thrown", "Eco-friendly", "Boho"]
materials = ["stoneware", "porcelain", "earthenware", "ceramic"]
tags_pool = ["handmade", "gift", "coffee", "kitchen", "ceramic", "boho", "minimalist"]

def mk_price():
    return round(random.uniform(12.0, 45.0), 2)

competitors = []
for i in range(20):
    title = f"{random.choice(adjectives)} {random.choice(base_titles)}"
    price = mk_price()
    tags = random.sample(tags_pool, k=3)
    # small description that might be useful to the LLM
    desc = f"{title} made of {random.choice(materials)} with {random.choice(['matte', 'glossy', 'speckled'])} finish."
    competitors.append({
        "id": f"synthetic-{i+1}",
        "title": title,
        "price": price,
        "tags": tags,
        "short_description": desc,
        "rating": round(random.uniform(3.5, 5.0), 2),
        "sales_count": random.randint(5, 500)
    })

payload = {
    "platform": "etsy",
    "competitors": competitors,
    "avg_price": round(sum(c["price"] for c in competitors) / len(competitors), 2),
    "source": "synthetic-demo"
}

with open("../data/synthetic_competitors_etsy.json", "w", encoding="utf-8") as f:
    json.dump(payload, f, indent=2)

print("Wrote data/synthetic_competitors_etsy.json")