## What I Did
I wrote 'getting_culture.py' to compare two APIs about Marvel Movies:

1. **MediaWiki Action API:** I searched the Marvel Cinematic Universe Fandom wiki for "Iron Man" and printed the results. 
2. **TMDB API:** I requested Marvel Studios movies released post 2008 on and printed them. 
3. **Connecting** For each TMDB movie, I searched for that title in the wiki and recorded the matching page. 

## Comparison

I compared the Marvel Cinematic Universe Fandom wiki with The Movide Database (TMDB). The wiki required no key or account, only a User-Agent identifying me. TMDB required an account, inclduing an application where I had to explain why I needed an API key. TMDB returned a clean JSON that recorded information on the movies which made it easy to get a list of movies . There were some gaps as TMDB had specific movie titles while the wiki had individual character pages and movies, but not all movies were represented (only movies considered a part of the MCU). Both websites are run by companies who get their funding from the website users. What's missing from these websites is the lesser known movies data, as movies like Iron Man are represented multiple times but lesser known movies aren't mentioned at all. 