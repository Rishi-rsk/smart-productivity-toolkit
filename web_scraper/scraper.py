import requests
from bs4 import BeautifulSoup
import csv

URL = "https://news.ycombinator.com/"  # simple + safe site

def fetch_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"[✗] Error fetching page: {e}")
        return None

def parse_html(html):
    soup = BeautifulSoup(html, "html.parser")
    titles = soup.find_all("span", class_="titleline")

    data = []
    for i, title in enumerate(titles, start=1):
        link = title.find("a")
        if link:
            text = link.text
            url = link.get("href")
            data.append((i, text, url))

    return data

def save_to_csv(data, filename="news.csv"):
    try:
        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Title", "URL"])
            writer.writerows(data)
        print(f"[✓] Data saved to {filename}")
    except Exception as e:
        print(f"[✗] Error saving file: {e}")

def display_data(data):
    print("\nTop News Headlines:\n")
    for item in data[:10]:
        print(f"{item[0]}. {item[1]}")
    print("\n")

def main():
    print("=" * 50)
    print("   🌐 Web Scraper - News Headlines")
    print("=" * 50)

    html = fetch_page(URL)
    if not html:
        return

    data = parse_html(html)
    display_data(data)
    save_to_csv(data)

if __name__ == "__main__":
    main()