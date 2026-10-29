import csv
import time
 
import requests
from bs4 import BeautifulSoup
from rich.console import Console
from rich.table import Table
 
 
BASE_URL = "https://tolkiengateway.net"
LITERARY_CATEGORY_URL = f"{BASE_URL}/wiki/Category:Characters_in_The_Lord_of_the_Rings"
ADAPTATION_CATEGORY_URL = f"{BASE_URL}/wiki/Category:The_Rings_of_Power_(TV_series)_characters"
RINGS_OF_POWER_PATH = "/wiki/The_Lord_of_the_Rings:_The_Rings_of_Power"
HEADERS = {
    "User-Agent": "is310-course-scraper/1.0 (student project; netid@illinois.edu)"
}  # Replace netid with your actual netid
REQUEST_DELAY = 1.0
RESULTS_OUTPUT = "tolkien_gateway_characters.csv"
 
console = Console()
 
 
def fetch_soup(url):
    if not url:
        console.print("[yellow]No URL was found for this page.[/yellow]")
        return None
 
    response = requests.get(url, headers=HEADERS, timeout=30)
    time.sleep(REQUEST_DELAY)
 
    if response.status_code != 200:
        console.print(f"[red]Could not download {url}: HTTP {response.status_code}[/red]")
        return None
 
    return BeautifulSoup(response.text, "html.parser")
 
 
def scrape_characters(category_page, source_url):
    characters = []
    if category_page is None:
        return characters
 
    characters_section = category_page.find(id="mw-pages")
    if characters_section is None:
        return characters
 
    if source_url == LITERARY_CATEGORY_URL:
        character_type = "literary"
    else:
        character_type = "adaptation"
 
    character_items = characters_section.find_all("li")
    for item in character_items:
        link = item.find("a", href=True)
        if link is None:
            continue
 
        characters.append({
            "character": link.get_text(" ", strip=True),
            "character_type": character_type,
            "source_url": source_url,
            "character_url": f"{BASE_URL}{link['href']}",
        })
 
    return characters
 
 
def get_internal_links(content):
    if content is None:
        return []
 
    links = []
    for link in content.find_all("a", href=True):
        href = link["href"]
        if href.startswith("/wiki/") and "#" not in href:
            links.append(href)
 
    return links
 
 
def analyze_character(character):
    soup = fetch_soup(character["character_url"])
    record = character.copy()
    record["word_count"] = 0
    record["character_count"] = 0
    record["internal_link_count"] = 0
    record["unique_internal_link_count"] = 0
    record["rings_of_power_link"] = False
 
    if soup is None:
        return record
 
    content = soup.select_one("#mw-content-text .mw-parser-output")
    if content is None:
        return record
 
    article_text = content.get_text(" ", strip=True)
    word_count = len(article_text.split())
    character_count = len(article_text)
    internal_links = get_internal_links(content)
    unique_internal_links = []
    for href in internal_links:
        if href not in unique_internal_links:
            unique_internal_links.append(href)
 
    record["word_count"] = word_count
    record["character_count"] = character_count
    record["internal_link_count"] = len(internal_links)
    record["unique_internal_link_count"] = len(unique_internal_links)
    if record["character_type"] == "literary":
        record["rings_of_power_link"] = RINGS_OF_POWER_PATH in internal_links
    return record
 
 
def save_csv(records, output_path):
    if not records:
        console.print(f"[yellow]No records to save to {output_path}[/yellow]")
        return
 
    with open(output_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)
 
 
def print_results_table(records):
    table = Table(title="Literary and Adaptation Character Pages")
    table.add_column("Character", style="cyan")
    table.add_column("Type", style="green")
    table.add_column("Literary Character in Rings of Power", style="magenta")
    table.add_column("Words", justify="right")
    table.add_column("Characters", justify="right")
    table.add_column("All Links", justify="right")
    table.add_column("Unique Links", justify="right")
 
    for record in sorted(records, key=lambda record: record["word_count"], reverse=True):
        table.add_row(
            record["character"],
            record["character_type"],
            str(record["rings_of_power_link"]),
            str(record["word_count"]),
            str(record["character_count"]),
            str(record["internal_link_count"]),
            str(record["unique_internal_link_count"]),
        )
 
    console.print(table)
 
 
def main():
    console.print("[cyan]Finding The Lord of the Rings characters...[/cyan]")
    literary_page = fetch_soup(LITERARY_CATEGORY_URL)
    literary_characters = scrape_characters(
        literary_page,
        LITERARY_CATEGORY_URL,
    )
 
    console.print("[cyan]Finding The Rings of Power characters...[/cyan]")
    adaptation_character_page = fetch_soup(ADAPTATION_CATEGORY_URL)
    adaptation_characters = scrape_characters(
        adaptation_character_page,
        ADAPTATION_CATEGORY_URL,
    )
 
    all_characters = literary_characters + adaptation_characters
    console.print(f"[green]Found {len(all_characters)} character pages.[/green]")
 
    results = []
    for number, character in enumerate(all_characters, start=1):
        console.print(f"Processing {number}/{len(all_characters)}: {character['character']}")
        results.append(analyze_character(character))
 
    print_results_table(results)
    save_csv(results, RESULTS_OUTPUT)
    console.print(f"[green]Saved {len(results)} analyzed character pages to {RESULTS_OUTPUT}[/green]")
 
 
if __name__ == "__main__":
    main()
