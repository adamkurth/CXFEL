import requests
from rcsbsearchapi.search import AttributeQuery

# Define the search criteria
space_group = "P1211"  # P1211 space group

# Define the API URL for searching PDB entries
search_url = "https://data.rcsb.org/rest/v1/search"

# Define the query to search for randomized structures in the specified space group
query = AttributeQuery("rcsb_struct_symmetry.space_group_name_H-M", "exact_match", "P 1 2 1 1")
# Make the API request to search for PDB entries
response = requests.get(search_url, params={"json": query})

if response.status_code == 200:
    data = response.json()
    pdb_ids = data.get("result_set", [])
    print(f"Randomized PDB IDs in space group {space_group}:")
    for pdb_id in pdb_ids:
        print(pdb_id)
else:
    print(f"Error: Unable to retrieve PDB data. Status code {response.status_code}")
