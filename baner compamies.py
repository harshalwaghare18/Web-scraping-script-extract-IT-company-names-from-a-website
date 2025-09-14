import requests
from bs4 import BeautifulSoup
import pandas as pd

URL = "https://punelist.com/2020/10/list-of-it-companies-in-bavdhan-punelist.html#google_vignette"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
    AppleWebKit/537.36 (KHTML, like Gecko) \
    Chrome/119.0.0.0 Safari/537.36"
}

def fetch_page(url):
    resp = requests.get(url, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    return resp.text

def parse_companies(html):
    soup = BeautifulSoup(html, "html.parser")
    companies = []

    for tag in soup.find_all("strong"):
        text = tag.get_text(strip=True)
        if text and text[0].isdigit():  # only numbered entries
            parts = text.split(".", 1)
            if len(parts) > 1:
                name = parts[1].strip()
                companies.append({"Company Name": name})
    return companies

def main():
    html = fetch_page(URL)
    companies = parse_companies(html)

    df = pd.DataFrame(companies)
    output_file = "IT_Companies_Bavdhan.xlsx"
    df.to_excel(output_file, index=False)

    print(f"✅ Saved {len(companies)} company names to {output_file}")

if __name__ == "__main__":
    main()

