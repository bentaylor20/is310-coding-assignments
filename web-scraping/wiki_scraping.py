import csv
import time
import requests
from bs4 import BeautifulSoup
from rich.console import Console
from rich.table import Table

BASE_URL = "https://bulbapedia.bulbagarden.net"
TYPES = [
    "Normal", "Fire", "Water", "Electric", "Grass", "Ice",
    "Fighting", "Poison", "Ground", "Flying", "Psychic",
    "Bug", "Rock", "Ghost", "Dragon", "Dark", "Steel", "Fairy"
]
HEADERS = {
    "User-Agent": "is310-course-scraper/1.0 (student project; bent5@illinois.edu)"
}
REQUEST_DELAY = 5.0
PAGES_PER_TYPE = 10
PAGES_OUTPUT = "bulbapedia_pokemon.csv"
SUMMARY_OUTPUT = "bulbapedia_type_summary.csv"

console = Console()

def fetch_soup(url):
    if not url:
        console.print("No URL was found for this page.")
        return None
    response = requests.get(url, headers=HEADERS, timeout=30)
    time.sleep(REQUEST_DELAY)

    if response.status_code != 200:
        console.print("Could not download {url}: HTTP {response.status_code}")
        return None
    return BeautifulSoup(response.text, "html.parser")

def get_type_category_url(type_name):
    return f"{BASE_URL}/wiki/Category:{type_name}-type_Pokémon"

def scrape_pokemon(category_page, type_name, source_url):
    pokemon = []
    if category_page is None:
        return pokemon

    pokemon_section = category_page.find(id="mw-pages")
    if pokemon_section is None:
        return pokemon

    pokemon_items = pokemon_section.find_all("li")
    for item in pokemon_items:
        link = item.find("a", href=True)
        if link is None:
            continue
        
        pokemon.append({
            "pokemon": link.get_text(" ", strip=True),
            "type": type_name,
            "source_url": source_url,
            "pokemon_url": f"{BASE_URL}{link['href']}",
        })

    return pokemon

def find_next_page_url(category_page):
    if category_page is None:
        return None

    pokemon_section = category_page.find(id="mw-pages")
    if pokemon_section is None:
        return None

    next_link = pokemon_section.find("a", string="next page")
    if next_link is None:
        return None

    return f"{BASE_URL}{next_link['href']}"

def scrape_type(type_name):
    all_pokemon = []
    url = get_type_category_url(type_name)
    while url:
        category_page = fetch_soup(url)
        all_pokemon = all_pokemon + scrape_pokemon(category_page, type_name, url)
        url = find_next_page_url(category_page)
    return all_pokemon

def get_internal_links(content):
    if content is None:
        return []

    links = []
    for link in content.find_all("a", href=True):
        href = link["href"]
        if href.startswith("/wiki/") and "#" not in href:
            links.append(href)

    return links

def analyze_pokemon(pokemon):
    soup = fetch_soup(pokemon["pokemon_url"])
    record = pokemon.copy()
    record["word_count"] = 0
    record["pokemon_count"] = 0
    record["internal_link_count"] = 0
    record["unique_internal_link_count"] = 0

    if soup is None:
        return record

    content = soup.select_one("#mw-content-text .mw-parser-output")
    if content is None:
        return record

    article_text = content.get_text(" ", strip=True)
    word_count = len(article_text.split())
    pokemon_count = len(article_text)
    internal_links = get_internal_links(content)
    unique_internal_links = []
    for href in internal_links:
        if href not in unique_internal_links:
            unique_internal_links.append(href)

    record["word_count"] = word_count
    record["pokemon_count"] = pokemon_count
    record["internal_link_count"] = len(internal_links)
    record["unique_internal_link_count"] = len(unique_internal_links)
    return record

def summarize_type(type_name, pokemon_count, records):
    # Pages that failed to download have word_count 0, so we leave them out of averages.
    measured = []
    for record in records:
        if record["word_count"] > 0:
            measured.append(record)
 
    total_words = 0
    total_unique_links = 0
    for record in measured:
        total_words += record["word_count"]
        total_unique_links += record["unique_internal_link_count"]
 
    average_words = 0
    average_unique_links = 0
    if measured:
        average_words = round(total_words / len(measured), 1)
        average_unique_links = round(total_unique_links / len(measured), 1)
 
    return {
        "type": type_name,
        "pokemon_in_category": pokemon_count,
        "pages_measured": len(measured),
        "average_word_count": average_words,
        "average_unique_internal_links": average_unique_links,
    }


def save_csv(records, output_path):
    if not records:
        console.print("No records to save to {output_path}")
        return

    with open(output_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)

def print_summary_table(summaries):
    table = Table(title="Pokemon Types on Bulbapedia")
    table.add_column("Type", style="cyan")
    table.add_column("Pokemon in Type", justify="right")
    table.add_column("Pages Measured", justify="right")
    table.add_column("Avg Words", justify="right")
    table.add_column("Avg Unique Links", justify="right")

    for summary in sorted(summaries, key=lambda summary: summary["pokemon_in_category"], reverse=True):
        table.add_row(
            summary["type"],
            str(summary["pokemon_in_category"]),
            str(summary["pages_measured"]),
            str(summary["average_word_count"]),
            str(summary["average_unique_internal_links"]),
        )
    console.print(table)

def main():
    measured_pages = {}  # a dual-type Pokémon appears in two categories; fetch it once
    page_records = []
    summaries = []
 
    for type_name in TYPES:
        console.print(f"Finding {type_name}-type Pokémon...")
        type_pokemon = scrape_type(type_name)
        console.print(f"Found {len(type_pokemon)} {type_name}-type Pokémon.")
 
        sample = type_pokemon[:PAGES_PER_TYPE]
        type_records = []
        for number, pokemon in enumerate(sample, start=1):
            console.print(f"Processing {type_name} {number}/{len(sample)}: {pokemon['pokemon']}")
            url = pokemon["pokemon_url"]
            if url not in measured_pages:
                measured_pages[url] = analyze_pokemon(pokemon)
            record = measured_pages[url].copy()
            record["type"] = type_name
            type_records.append(record)
 
        page_records = page_records + type_records
        summaries.append(summarize_type(type_name, len(type_pokemon), type_records))
 
    print_summary_table(summaries)
    save_csv(page_records, PAGES_OUTPUT)
    save_csv(summaries, SUMMARY_OUTPUT)
    console.print(f"Saved {len(page_records)} page measurements to {PAGES_OUTPUT}")
    console.print(f"Saved type summary to {SUMMARY_OUTPUT}")
 
 
if __name__ == "__main__":
    main()
    
