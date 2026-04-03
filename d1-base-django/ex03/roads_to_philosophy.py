import sys
import requests
from bs4 import BeautifulSoup

# python3 -m venv venv
# source venv/bin/activate
# pip install -r requirement.txt

def parse_arguments():
  if len(sys.argv) != 2:
      print("Erreur: Commandes attendues: python3 roads_to_philosophy.py <mot>")
      sys.exit(1)
  return sys.argv[1]

def is_valid_link(link):
    href = link.get('href', '')
    if not href.startswith('/wiki/'):
        return False
    if any(prefix in href for prefix in ['/wiki/Help:', '/wiki/Wikipedia:', '/wiki/File:', '/wiki/Special:']):
        return False
    return True

def find_first_valid_link(paragraph):
  paragraphs = paragraph.find_all('a', recursive=False)
  for link in paragraphs:
      if is_valid_link(link):
          return link
  return None

def get_intro_paragraphs(soup):
    content = soup.find("div", id="mw-content-text")
    if not content:
        print("Erreur: Contenu principal introuvable.")
        return []

    parser_output = content.find("div", class_="mw-parser-output")
    if not parser_output:
        print("Erreur: mw-parser-output introuvable.")
        return []

    intro_paragraphs = []

    for element in parser_output.descendants:
        if element.name == "h2":
            break

        if element.name == "p":
            if element.find_parent(["table", "aside"]):
                continue

            text = element.get_text(strip=True)
            if text:
                intro_paragraphs.append(element)

    return intro_paragraphs

def get_wikipedia_page_soup(keyword):
    url = "https://en.wikipedia.org/wiki/" + keyword.replace(" ", "_")
    headers = {
        "User-Agent": "cestmoijesuisgentille"
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"It's a dead end !")
        sys.exit(1)
    return BeautifulSoup(response.text, "html.parser")

def road_to_philosophy(search):
  soup = get_wikipedia_page_soup(search)
  intro_paragraphs = get_intro_paragraphs(soup)
  title = soup.find(id="firstHeading").text
  visited_pages = set()
  philosophie = "Philosophy"

  print(title)
  if title == philosophie:
      print("1 road straight to philosophy !")
      return
  while title != philosophie:
    if title in visited_pages:
        print("It leads to an infinite loop !")
        return
    visited_pages.add(title)

    first_link = None
    for paragraph in intro_paragraphs:
        first_link = find_first_valid_link(paragraph)
        if first_link:
            break

    if not first_link:
        print("It leads to a dead end !")
        return

    soup = get_wikipedia_page_soup(first_link['href'].split('/wiki/')[1])
    intro_paragraphs = get_intro_paragraphs(soup)
    title = soup.find(id="firstHeading").text
    print(title)

  print(f"{len(visited_pages)} roads from {search} to philosophy !")
  return

if __name__ == "__main__":
  search = parse_arguments()
  road_to_philosophy(search)
