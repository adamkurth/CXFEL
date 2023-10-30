import requests
import random

# Define the query parameters for the RCSB PDB API
api_url = "https://www.rcsb.org/pdb/rest/search"
query_params = {
    "version": 1,
    "query": "(space_group_name_H-M='P 1 21 1') AND (type_of_experiment=x-ray)",
    "return_type": "entry"
}

# Send a request to the API to get a list of PDB IDs
response = requests.get(api_url, params=query_params)

# Check if the request was successful
if response.status_code == 200:
    # Parse the response and extract the list of PDB IDs
    pdb_ids = response.text.split()

    # Randomly select a PDB ID from the list
    if pdb_ids:
        selected_pdb_id = random.choice(pdb_ids)
        print(f"Selected PDB ID in P1211 space group: {selected_pdb_id}")
    else:
        print("No PDB IDs found in P1211 space group.")
else:
    print("Failed to retrieve PDB IDs from the RCSB PDB API.")
