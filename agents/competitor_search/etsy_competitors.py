import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from bs4 import BeautifulSoup
from typing import Dict, List
from models.product import Product
from playwright.sync_api import sync_playwright


class EtsyCompetitorResearchAgent:
    BASE_URL = "https://www.etsy.com/search?q="

    def fetch_competitors(self, product: Product) -> Dict:
        query = product.title.replace(" ", "+")
        url = f"{self.BASE_URL}{query}"

        with sync_playwright() as p:
                browser = p.chromium.launch(headless=False)  # keep visible for now
                context = browser.new_context(
                    user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                            "AppleWebKit/537.36 (KHTML, like Gecko) "
                            "Chrome/120.0.0.0 Safari/537.36"
                )
                page = context.new_page()
                page.goto(url, timeout=30_000)

                try:
                    page.wait_for_selector("li.wt-list-unstyled", timeout=15_000)
                except Exception as e:
                    print("WARNING: selector not found:", e)

                html = page.content()
                
                # DEBUG: write first 5k chars of HTML to file
                with open("etsy_debug.html", "w", encoding="utf-8") as f:
                    f.write(html[:5000])
                print("DEBUG: wrote etsy_debug.html")

                browser.close()

        soup = BeautifulSoup(html, "html.parser")

        competitors: List[Dict] = []
        for item in soup.select("li.wt-list-unstyled")[:10]:
            title = item.select_one("h3")
            price = item.select_one("span.currency-value")
            if not title or not price:
                continue
            competitors.append({
                "title": title.get_text(strip=True),
                "price": float(price.get_text(strip=True).replace(",", "")),
                "tags": []
            })

        if not competitors:
            return {"platform": "etsy", "competitors": [], "avg_price": 0.0, "error": "No competitors found"}

        avg_price = sum(c["price"] for c in competitors) / len(competitors)
        return {
            "platform": "etsy",
            "competitors": competitors,
            "avg_price": round(avg_price, 2)
        }

    #def fetch_competitors(self, product: Product) -> Dict:
    #    query = product.title.replace(" ", "+")
    #    url = f"{self.BASE_URL}{query}"
    #    headers = {
    #        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    #                    "AppleWebKit/537.36 (KHTML, like Gecko) "
    #                    "Chrome/124.0.0.0 Safari/537.36",
    #        "Accept-Language": "en-US,en;q=0.9",
    #        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    #        "Referer": "https://www.google.com/",
    #       "DNT": "1",  # Do Not Track
    #    }

     #   response = requests.get(url, headers=headers)
     #   print("STATUS:", response.status_code, "URL:", response.url)
     #   print("HTML snippet:\n", response.text[:500])

     #   if response.status_code != 200:
     #       return {"platform": "etsy", "competitors": [], "avg_price": 0.0, "error": "Failed to fetch search results"}
        
     #   soup = BeautifulSoup(response.text, "html.parser")

        # Extract competitor listings
     #   competitors: List[Dict] = []
     #   for item in soup.select("li.wt-list-unstyled")[:10]:  # top 10 results
     #       title = item.select_one("h3")
     #       price = item.select_one("span.currency-value")

      #      if not title or not price:
      #          continue
#
       #     competitors.append({
       #         "title": title.get_text(strip=True),
      #          "price": float(price.get_text(strip=True).replace(",", "")),
       #         "tags": []  # Etsy search page doesn’t show tags directly
       #     })

       # print(response.text[:2000])

       # if not competitors:
       #     return {"platform": "etsy", "competitors": [], "avg_price": 0.0, "error": "No competitors found"}

       # avg_price = sum(c["price"] for c in competitors) / len(competitors)

        #return {
        #    "platform": "etsy",
        #    "competitors": competitors,
        #    "avg_price": round(avg_price, 2)
       # }

        
    