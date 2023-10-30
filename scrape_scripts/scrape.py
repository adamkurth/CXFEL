import requests
from bs4 import BeautifulSoup

def scrape_structure_factor_weight(pdb_id):
    url = f"https://www.rcsb.org/structure/{pdb_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error: Unable to fetch data from the provided URL.")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the Macromolecule Content section
    macromolecule_section = soup.find('div', {'id': 'macromolecule-content'})

    if macromolecule_section:
        # Search for the "Total Structure Weight" text and extract the weight
        total_structure_weight = None
        for item in macromolecule_section.find_all('li'):
            if "Total Structure Weight" in item.get_text():
                total_structure_weight = item.get_text().split(":")[-1].strip()
                break

        if total_structure_weight:
            return total_structure_weight

    print("No 'Total Structure Weight' data found under Macromolecule Content on the provided webpage.")
    return None

if __name__ == "__main__":
    pdb_id = "12E8"  # Replace with the PDB ID you want to scrape
    structure_weight = scrape_structure_factor_weight(pdb_id)

    if structure_weight:
        print(f"Total Structure Weight: {structure_weight}")
