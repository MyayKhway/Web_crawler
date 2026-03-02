import re

def extract_director(text):
    match = re.search(r'Directed by\s*\n\s*(.+?)(?:\n[A-Z])', text, re.DOTALL)
    return match.group(1).strip() if match else "N/A"

def extract_starring(text):
    section = re.search(r'Starring\s*\n(.+?)(?:\nCinematography|\nProduction|\nDirected|\nMusic|\nEdited)', text, re.DOTALL)
    if section:
        names = [line.strip() for line in section.group(1).splitlines() if line.strip()]
        return ', '.join(names)
    return "N/A"

def extract_production_companies(text):
    match = re.search(r'Production\s*companies?\s*\n\s*(.+?)(?:\n[A-Z][a-z])', text, re.DOTALL)
    if match:
        companies = [line.strip() for line in match.group(1).splitlines() if line.strip()]
        return ', '.join(companies)
    return "N/A"

def extract_distributor(text):
    match = re.search(r'Distributed by\s*\n\s*(.+?)(?:\n[A-Z])', text, re.DOTALL)
    if match:
        names = [line.strip() for line in match.group(1).splitlines() if line.strip()]
        return ', '.join(names)
    return "N/A"

def extract_running_time(text):
    match = re.search(r'(\d+)\s*minutes?', text)
    return f"{match.group(1)} minutes" if match else "N/A"

def extract_country(text):
    match = re.search(r'Countr(?:y|ies)\s*\n\s*(.+?)(?:\nLanguage|\nBudget|\nBased)', text, re.DOTALL)
    if match:
        return ', '.join(line.strip() for line in match.group(1).splitlines() if line.strip())
    return "N/A"

def extract_budget(text):
    match = re.search(r'Budget\s*\n\s*((?:\$|₩|€|£)[\d,]+(?:\.\d+)?\s*(?:million|billion|thousand)?)', text, re.IGNORECASE)
    return match.group(1).strip() if match else "N/A"

def extract_box_office(text):
    match = re.search(r'Box\s*office\s*\n\s*((?:\$|₩|€|£)[\d,]+(?:\.\d+)?\s*(?:million|billion|thousand)?)', text, re.IGNORECASE)
    return match.group(1).strip() if match else "N/A"

def extract_language(text):
    match = re.search(r'Language(?:s)?\s*\n\s*(.+?)(?:\nBudget|\nBox office|\nRelease|\nCinematography)', text, re.DOTALL)
    if match:
        return ', '.join(line.strip() for line in match.group(1).splitlines() if line.strip())
    return "N/A"


def extract_film_data(url):
    import requests
    from bs4 import BeautifulSoup

    HEADERS = {'User-Agent': 'Mozilla/5.0 (compatible; OscarFilmScraper/1.0)'}
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        infobox = soup.find('table', {'class': 'infobox'})
        if not infobox:
            return None

        text = infobox.get_text(separator='\n')  # critical — prevents field bleeding

        return {
            'director':             extract_director(text),
            'starring':             extract_starring(text),
            'production_companies': extract_production_companies(text),
            'distributor':          extract_distributor(text),
            'running_time':         extract_running_time(text),
            'country':              extract_country(text),
            'budget':               extract_budget(text),
            'box_office':           extract_box_office(text),
            'language':             extract_language(text),
        }
    except Exception as e:
        print(f"Error: {e}")
        return None


if __name__ == "__main__":
    test_films = [
        ("The Brutalist",  "https://en.wikipedia.org/wiki/The_Brutalist_(film)"),
        ("No Country for Old Men", "https://en.wikipedia.org/wiki/No_Country_for_Old_Men"),
        ("Parasite",       "https://en.wikipedia.org/wiki/Parasite_(2019_film)"),
    ]
    for title, url in test_films:
        print(f"\n{'='*50}\nTesting: {title}\n{'='*50}")
        data = extract_film_data(url)
        if data:
            for key, value in data.items():
                print(f"  {'✓' if value != 'N/A' else '✗ N/A'}  {key}: {value}")
        else:
            print("  ✗ Failed")