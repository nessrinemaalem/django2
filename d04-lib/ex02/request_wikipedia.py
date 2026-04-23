import sys
import requests
import dewiki

# python3 -m venv venv
# source venv/bin/activate
# pip install -r requirement.txt

def parse_arguments():
  if len(sys.argv) != 2:
      print("Erreur: Commandes attendues: python3 request_wikipedia.py <recherche>")
      sys.exit(1)
  return sys.argv[1]


def search_keyword(keyword):

  url = (
    "https://fr.wikipedia.org/w/api.php"
    "?action=query"
    "&list=search"
    f"&srsearch={keyword}"
    "&format=json"
  )

  headers = {
    "User-Agent": "cestmoijesuisgentille"
  }

  try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
  except requests.RequestException as e:
    print(f"Erreur lors de la requête HTTP : {e}")
    sys.exit(1)

  data = response.json()

  search = data.get("query", {}).get("search", {})
  if not search:
      print("Erreur : mot cle invalide")
      sys.exit(1)

  result = search[0]["title"]
  
  if not result:
      print("Erreur : resulat introuvable.")
      sys.exit(1)

  return result

def fetch_wikipedia_summary(title):

  url = (
    "https://fr.wikipedia.org/w/api.php"
    "?action=query"
    "&prop=extracts|categories"
    "&explaintext"
    "&exintro"
    f"&titles={title}"
    "&clshow=!hidden"
    "&cllimit=10"
    "&format=json"
  )

  headers = {
    "User-Agent": "cestmoijesuisgentille"
  }

  try:
      response = requests.get(url, headers=headers)
      response.raise_for_status()
  except requests.RequestException as e:
      print(f"Erreur lors de la requête HTTP : {e}")
      sys.exit(1)

  data = response.json()

  pages = data.get("query", {}).get("pages", {})
  if not pages:
      print("Erreur : article non trouvé.")
      sys.exit(1)

  page = next(iter(pages.values()))
  summary = page.get("extract", "")
  
  if not summary:
      print("Erreur : résumé vide.")
      sys.exit(1)

  categories = page.get("categories", [])[:2]

  if categories:
      for cat in categories:
          nom = cat["title"].replace("Catégorie:", "Categorie:")
          summary += f"\n\n{nom}"
  return summary


def clean_text(text):
  cleaned = dewiki.from_string(text)
  return (cleaned)

if __name__ == "__main__":
  keyword = parse_arguments()
  first_result = search_keyword(keyword)
  summary = fetch_wikipedia_summary(first_result)
  cleaned_summary = clean_text(summary)
  file_title = f"{keyword.replace(' ', '_')}.wiki"
  with open(file_title, "w", encoding="utf-8") as f:
      f.write(cleaned_summary)
