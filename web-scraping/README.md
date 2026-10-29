# Bulbapedia Scraping: Pokemon Types

## Wiki and Question
I scraped Bulbapedia, the community-run Pokemon wiki.

My main question was "Which Pokemon types are most represented on Bulbapedia, both in how many Pokemon are there of each type and how much documentation each type receives?

I chose this because I grew up playing the Pokemon games and still find the Pokemon community very interesting. I know there's been new types added over the years and that certain types are more valuable than others, so I thought it would be interesting to see if the more powerful types are more or less common. 

## robots.txt

Link: 'https://bulbapedia.bulbagarden.net/robots.txt'

The robots.txt on Bulbapedia allows wiki pages. It doesn't allow search pages, random pages, page-history pages, and old revisions. It also asks for a delat of 5 second between requests so I built my scraper to include that. 

## What my scraper does

'wiki_scraping.py' uses 'requests' and 'BeautifulSoup'

It starts by reading the category page for each Pokeemon type and counting the number of pokemon listed.

It then finds the first 10 pokemon listed in each type and visits their page and counts the words, characters, internal links, and unique internal links. 

It ends by saving the results to bulbapedia_type_summary.csv' and 'bulbapedia_pokemon.csv'.

## Reflection

My data counts how many Pokemon are identified in each type, plus the length and links of a small sample of Pokemon pages. These are proxies for representation and popularity, not actual measures. A type with many pokemon is not necessarily more popular within the community or more important. Pokemon with dual types are also counted twice. Longer pages that include more links might just represent an older Pokemon rather than a more popular Pokemon. My scraper also only looks at the first 10 pokemon per type, alphabetically. It cannot be concluded from the scraped data that the type with the most Pokemon or the longest pages is the communities favorite or most important/impactful type.