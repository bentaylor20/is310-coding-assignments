import csv
 
from bs4 import BeautifulSoup
import requests
 
response = requests.get("https://www.gutenberg.org/browse/scores/top")
print("Status code:", response.status_code)
 
soup = BeautifulSoup(response.text, "html.parser")
top_lists = soup.find_all("h2")
 
books = []
authors = []
 
for top_list in top_lists:
    top_list_name = top_list.get_text()
    top_list_items = top_list.find_next('ol').find_all('li')
    for item in top_list_items:
        if "EBooks" in top_list_name:
            books.append({"top_list": top_list_name, "book_title": item.get_text(), "book_link": item.find('a').get('href')})
        else:
            authors.append({"top_list": top_list_name, "author_name": item.get_text(), "author_link": item.find('a').get('href')})
 
with open('top_100_ebooks.csv', 'w') as file:
    writer = csv.writer(file)
    # Write the headers
    writer.writerow(['top_list', 'book_title', 'book_link'])
    for book in books:
        writer.writerow([book['top_list'], book['book_title'], book['book_link']])
 
with open('top_100_authors.csv', 'w') as file:
    writer = csv.writer(file)
    # Write the headers
    writer.writerow(['top_list', 'author_name', 'author_link'])
    for author in authors:
        writer.writerow([author['top_list'], author['author_name'], author['author_link']])
 
 
# Links on this page are relative (e.g. /ebooks/84), so we add the base URL.
def check_gutenberg_page_exists(url):
    gutenberg_url = "https://www.gutenberg.org" + url
    response = requests.get(gutenberg_url)
    if response.status_code == 200:
        return True
    else:
        return False
