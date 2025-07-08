import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www2.hm.com"
CATEGORY_URL = BASE_URL + "/en_in/men/new-arrivals/clothes.html"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def fetch_hm_products(pages=1):
    products = []

    for page in range(1, pages + 1):
        url = f"{CATEGORY_URL}?page-size=60&page={page}"
        print(f"Fetching: {url}")
        res = requests.get(url, headers=HEADERS, timeout=10)

        if res.status_code != 200:
            print(f"Failed to fetch page {page}")
            continue

        soup = BeautifulSoup(res.text, "html.parser")
        items = soup.select("li.product-item, article.product-item")

        for item in items:
            name_tag = item.select_one(".item-heading, .product-item-headline, h3")
            name = name_tag.get_text(strip=True) if name_tag else None

            a_tag = item.find("a", href=True)
            link = BASE_URL + a_tag['href'] if a_tag else None

            category = item.get("data-category") or item.get("data-analytics-category") or ""

            img_tag = item.find("img")
            image = img_tag.get("src") or img_tag.get("data-src") if img_tag else None

            if name and link:
                products.append({
                    "name": name,
                    "category": category,
                    "link": link,
                    "image_url": image
                })

    print(f"✅ Fetched {len(products)} products.")
    return products


if __name__ == "__main__":
    data = fetch_hm_products(pages=1)
    for d in data[:5]:
        print(d)


