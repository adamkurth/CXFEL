import requests
import random

import requests
import random

# Define the RCSB PDB API endpoint for the search
api_url = "https://www.rcsb.org/pdb/graphql"
query = {
    "query": {
        "type": "group",
        "logical_operator": "and",
        "nodes": [
            {
                "type": "terminal",
                "service": "text",
                "parameters": {
                    "attribute": "rcsb_entry_info.space_group_name_H-M",
                    "operator": "exact_match",
                    "value": "P 1 21 1"               
                }
            }
        ]
    },
    "return_type": "entry",
    "request_options": {
        "results_content_type": ["experimental"]
    }
}

# Send the GraphQL query to the RCSB PDB API
response = requests.post(api_url, json=query)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    entry_list = data.get("data", {}).get("search", {}).get("edges", [])
    
    if entry_list:
        # Extract PDB IDs from the search results
        pdb_ids = [entry["node"]["rcsb_entry_info"]["entry_id"] for entry in entry_list]
        
        # Randomly select a PDB ID from the list
        selected_pdb_id = random.choice(pdb_ids)
        print(f"Randomly selected PDB ID with space group 'P1211': {selected_pdb_id}")
    else:
        print("No PDB IDs found with the specified space group.")
else:
    print("Failed to retrieve PDB IDs from the RCSB PDB API.")
